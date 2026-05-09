import os
import uuid
from datetime import datetime, timezone

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from auth import get_current_user
from database import (
    create_order, update_order_stripe_session,
    complete_order, get_user_orders,
)

router = APIRouter(prefix="/api/payment", tags=["payment"])

PLANS = {
    "monthly": {
        "name": "VidDownAI VIP 月度会员",
        "amount": 990,
        "currency": "cny",
    },
}


class CreateCheckoutRequest(BaseModel):
    plan_type: str = "monthly"


def _generate_order_no(user_id: int) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]
    return f"SA{ts}{user_id:04d}{short_uuid}"


# ── 创建 Checkout Session ────────────────────────────────

@router.post("/create-checkout")
async def create_checkout_session(
    req: CreateCheckoutRequest,
    user: dict = Depends(get_current_user),
):
    secret_key = os.getenv("STRIPE_SECRET_KEY")
    price_id = os.getenv("STRIPE_PRICE_ID_MONTHLY")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

    if not secret_key or not price_id:
        raise HTTPException(status_code=500, detail="支付服务未配置")

    plan = PLANS.get(req.plan_type)
    if not plan:
        raise HTTPException(status_code=400, detail="无效的套餐类型")

    stripe.api_key = secret_key

    # 1. 创建本地订单
    order_no = _generate_order_no(user["id"])
    create_order(
        user_id=user["id"],
        order_no=order_no,
        amount=plan["amount"],
        currency=plan["currency"],
        plan_type=req.plan_type,
    )

    # 2. 创建 Stripe Checkout Session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=f"{frontend_url}?payment=success&order_no={order_no}",
            cancel_url=f"{frontend_url}?payment=cancel&order_no={order_no}",
            client_reference_id=str(user["id"]),
            customer_email=user["email"],
            metadata={
                "order_no": order_no,
                "user_id": str(user["id"]),
                "plan_type": req.plan_type,
            },
        )

        # 3. 保存 Stripe Session ID
        update_order_stripe_session(order_no, session.id)

        return {
            "success": True,
            "data": {
                "checkout_url": session.url,
                "order_no": order_no,
                "session_id": session.id,
            },
        }

    except stripe.StripeError as e:
        raise HTTPException(status_code=400, detail=f"创建支付会话失败: {str(e)}")


# ── Webhook 回调处理 ──────────────────────────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Stripe Webhook 回调处理。
    幂等性由 complete_order 保证：只有 pending 状态的订单才会被处理。
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        return JSONResponse(status_code=400, content={"error": "Webhook secret not configured"})

    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})
    except stripe.SignatureVerificationError:
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            payment_intent_id = session.get("payment_intent", "")
            result = complete_order(session["id"], payment_intent_id)

    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        payment_intent_id = session.get("payment_intent", "")
        complete_order(session["id"], payment_intent_id)

    return JSONResponse(status_code=200, content={"received": True})


# ── 订单历史 ──────────────────────────────────────────────

@router.get("/orders")
async def list_orders(user: dict = Depends(get_current_user)):
    orders = get_user_orders(user["id"])
    return {
        "success": True,
        "data": orders,
    }
