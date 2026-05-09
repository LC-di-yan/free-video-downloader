"""AI 视频总结相关 API 路由"""

import asyncio
import json
from collections.abc import AsyncIterable

from fastapi import APIRouter, Depends, HTTPException
from fastapi.sse import ServerSentEvent, EventSourceResponse
from pydantic import BaseModel

from auth import get_optional_user
from database import check_and_increment_summary, FREE_DAILY_SUMMARY_LIMIT

router = APIRouter(prefix="/api", tags=["AI 总结"])


class SummarizeRequest(BaseModel):
    url: str
    language: str = "zh"


class ChatRequest(BaseModel):
    url: str
    question: str
    subtitle_text: str = ""


def _check_summary_permission(user: dict | None):
    """检查 AI 总结权限"""
    if not user:
        return False, 0, "请先登录后使用 AI 总结功能"

    allowed, remaining = check_and_increment_summary(user["id"])
    if not allowed:
        return False, 0, f"今日免费次数已用完（每日 {FREE_DAILY_SUMMARY_LIMIT} 次），开通 VIP 可无限使用"

    return True, remaining, None


def _get_summarizer():
    """延迟初始化 VideoSummarizer"""
    from summarizer import VideoSummarizer
    if not hasattr(_get_summarizer, "_instance"):
        try:
            _get_summarizer._instance = VideoSummarizer()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return _get_summarizer._instance


def _get_extractor():
    """延迟初始化 SubtitleExtractor"""
    from summarizer import SubtitleExtractor
    if not hasattr(_get_extractor, "_instance"):
        _get_extractor._instance = SubtitleExtractor()
    return _get_extractor._instance


async def _run_in_thread(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


# ── 流式总结端点 ────────────────────────────────────────

@router.post("/summarize", response_class=EventSourceResponse)
async def summarize_video(
    req: SummarizeRequest,
    user: dict | None = Depends(get_optional_user),
) -> AsyncIterable[ServerSentEvent]:
    """
    AI 视频总结（SSE 流式）
    事件顺序：subtitle → summary(流式token) → mindmap → quota → done
    """
    allowed, remaining, message = _check_summary_permission(user)
    if not allowed:
        yield ServerSentEvent(
            raw_data=json.dumps({
                "message": message,
                "need_login": user is None,
                "need_vip": user is not None,
            }, ensure_ascii=False),
            event="error",
        )
        return

    try:
        extractor = _get_extractor()
        subtitle_data = await _run_in_thread(extractor.extract, req.url)

        yield ServerSentEvent(
            raw_data=json.dumps(subtitle_data, ensure_ascii=False),
            event="subtitle",
        )

        if not subtitle_data["has_subtitle"]:
            yield ServerSentEvent(
                raw_data=json.dumps({"message": "该视频没有可用的字幕，无法生成总结"}, ensure_ascii=False),
                event="error",
            )
            return

        full_text = subtitle_data["full_text"]

        # 流式生成总结摘要
        summarizer = _get_summarizer()
        for token in summarizer.summarize_stream(full_text, req.language):
            yield ServerSentEvent(
                raw_data=json.dumps(token, ensure_ascii=False),
                event="summary",
            )

        # 生成思维导图（非流式）
        mindmap_md = await _run_in_thread(summarizer.generate_mindmap, full_text, req.language)
        yield ServerSentEvent(
            raw_data=json.dumps({"markdown": mindmap_md}, ensure_ascii=False),
            event="mindmap",
        )

        # 发送剩余次数
        yield ServerSentEvent(
            raw_data=json.dumps({
                "remaining": remaining,
                "limit": FREE_DAILY_SUMMARY_LIMIT,
            }, ensure_ascii=False),
            event="quota",
        )

        yield ServerSentEvent(raw_data="[DONE]", event="done")

    except HTTPException:
        raise
    except Exception as e:
        yield ServerSentEvent(
            raw_data=json.dumps({"message": f"总结失败: {str(e)}"}, ensure_ascii=False),
            event="error",
        )


# ── AI 问答端点 ──────────────────────────────────────────

@router.post("/chat", response_class=EventSourceResponse)
async def chat_with_video(
    req: ChatRequest,
    user: dict | None = Depends(get_optional_user),
) -> AsyncIterable[ServerSentEvent]:
    """AI 视频问答（SSE 流式）"""
    try:
        if not req.subtitle_text.strip():
            extractor = _get_extractor()
            subtitle_data = await _run_in_thread(extractor.extract, req.url)
            if not subtitle_data["has_subtitle"]:
                yield ServerSentEvent(
                    raw_data=json.dumps({"message": "该视频没有可用的字幕，无法回答问题"}, ensure_ascii=False),
                    event="error",
                )
                return
            subtitle_text = subtitle_data["full_text"]
        else:
            subtitle_text = req.subtitle_text

        summarizer = _get_summarizer()
        for token in summarizer.chat_stream(subtitle_text, req.question):
            yield ServerSentEvent(
                raw_data=json.dumps(token, ensure_ascii=False),
                event="answer",
            )

        yield ServerSentEvent(raw_data="[DONE]", event="done")

    except HTTPException:
        raise
    except Exception as e:
        yield ServerSentEvent(
            raw_data=json.dumps({"message": f"回答失败: {str(e)}"}, ensure_ascii=False),
            event="error",
        )
