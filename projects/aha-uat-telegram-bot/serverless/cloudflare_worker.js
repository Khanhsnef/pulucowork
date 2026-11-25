/**
 * Cloudflare Worker Serverless Webhook cho Ahamove UAT Telegram Bot (Dự phòng 24/7)
 *
 * Biến môi trường (Environment Variables / Secrets trên Cloudflare Worker):
 * - AHA_BOT_TOKEN: Token của Telegram Bot (@sgmdmbot)
 * - AHA_GIST_ID: ID của Secret GitHub Gist lưu .tokens.json
 * - AHA_GIST_TOKEN: GitHub PAT có quyền gist
 * - AHA_DEFAULT_DRIVER_ID: "84981792046"
 *
 * Cách kích hoạt Webhook khi chuyển sang Cloudflare Worker:
 * curl "https://api.telegram.org/bot<AHA_BOT_TOKEN>/setWebhook?url=https://<worker-url>.workers.dev"
 */

const GIST_FILENAME = "aha_uat_tokens.json";
const USER_REFRESH_URL = "https://apiuat.ahamove.com/api/v3/public/user/token/refresh";
const ADMIN_REFRESH_URL = "https://apiuat.ahamove.com/api/v3/public/supplier/token/refresh";
const CREATE_ORDER_URL = "https://apiuat.ahamove.com/api/v3/private/order/create";

async function loadGistStore(env) {
  const resp = await fetch(`https://api.github.com/gists/${env.AHA_GIST_ID}`, {
    headers: {
      Authorization: `Bearer ${env.AHA_GIST_TOKEN}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "Ahamove-UAT-Telegram-Worker",
    },
  });
  const data = await resp.json();
  return JSON.parse(data.files[GIST_FILENAME].content);
}

async function saveGistStore(env, store) {
  await fetch(`https://api.github.com/gists/${env.AHA_GIST_ID}`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${env.AHA_GIST_TOKEN}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "Ahamove-UAT-Telegram-Worker",
    },
    body: JSON.stringify({
      files: { [GIST_FILENAME]: { content: JSON.stringify(store, null, 2) } },
    }),
  });
}

async function refreshUserToken(env, store) {
  const resp = await fetch(USER_REFRESH_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      refresh_token: store.user_refresh_token,
      mobile: store.user_mobile || "84981792046",
      type: "web",
      imei: store.user_imei || "lO10z54KkUncGeOyTPYo",
    }),
  });
  if (resp.ok) {
    const body = await resp.json();
    store.user_token = body.token;
    if (body.refresh_token) store.user_refresh_token = body.refresh_token;
    await saveGistStore(env, store);
  }
  return store.user_token;
}

async function refreshAdminToken(env, store) {
  const mobile = store.admin_mobile || "84981792046";
  const resp = await fetch(ADMIN_REFRESH_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      refresh_token: store.admin_refresh_token,
      mobile,
      supplier_id: mobile,
      type: "web",
      imei: "web",
      role: "admin",
    }),
  });
  if (resp.ok) {
    const body = await resp.json();
    store.admin_token = body.token;
    if (body.refresh_token) store.admin_refresh_token = body.refresh_token;
    await saveGistStore(env, store);
  }
  return store.admin_token;
}

async function tgSend(env, chatId, text) {
  await fetch(`https://api.telegram.org/bot${env.AHA_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text, parse_mode: "HTML" }),
  });
}

export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("Ahamove UAT Telegram Webhook Worker is running.", { status: 200 });
    }
    const update = await request.json();
    const msg = update.message;
    if (!msg || !msg.text) return new Response("OK");

    const chatId = msg.chat.id;
    const text = msg.text.trim();
    const parts = text.split(/\s+/);
    const cmd = parts[0].split("@")[0].toLowerCase();

    const store = await loadGistStore(env);
    const defaultDrv = store.default_driver_id || env.AHA_DEFAULT_DRIVER_ID || "84981792046";

    if (cmd === "/tao" || cmd === "/taogan") {
      const token = await refreshUserToken(env, store);
      const res = await fetch(CREATE_ORDER_URL, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
          Origin: "https://appuat.ahamove.com",
          Referer: "https://appuat.ahamove.com/",
        },
        body: JSON.stringify(store.order_template),
      });
      const body = await res.json();
      const orderId = body._id || body.order_id || (body.order && body.order._id);
      await tgSend(env, chatId, `✅ <b>Đã tạo đơn UAT:</b> <code>${orderId}</code>`);
      if (cmd === "/taogan" && orderId) {
        const drv = (parts[1] || defaultDrv).replace(/^0/, "84");
        const admToken = await refreshAdminToken(env, store);
        const aRes = await fetch(
          `https://adminv3uat.ahamove.com/api/orders/${orderId}/assign/${drv}`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${admToken}`,
              Origin: "https://adminv3uat.ahamove.com",
            },
          }
        );
        await tgSend(env, chatId, `🎉 <b>Gán đơn ${orderId} → ${drv}:</b> HTTP ${aRes.status}`);
      }
    } else if (cmd === "/gan" && parts.length >= 2) {
      const orderId = parts[1].toUpperCase();
      const drv = (parts[2] || defaultDrv).replace(/^0/, "84");
      const admToken = await refreshAdminToken(env, store);
      const aRes = await fetch(
        `https://adminv3uat.ahamove.com/api/orders/${orderId}/assign/${drv}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${admToken}`,
            Origin: "https://adminv3uat.ahamove.com",
          },
        }
      );
      await tgSend(env, chatId, `🎉 <b>Gán đơn ${orderId} → ${drv}:</b> HTTP ${aRes.status}`);
    }
    return new Response("OK");
  },
};
