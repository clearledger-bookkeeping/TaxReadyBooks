export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({success:false,error:"Method not allowed"});

  const {clientEmail, clientName, joinUrl} = req.body || {};
  if (!clientEmail || !joinUrl) return res.status(400).json({success:false,error:"Missing client email or call link"});

  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.RESEND_FROM_EMAIL;
  if (!apiKey || !from) return res.status(503).json({success:false,error:"Email service is not configured"});

  const response = await fetch("https://api.resend.com/emails", {
    method:"POST",
    headers:{
      "Authorization":"Bearer " + apiKey,
      "Content-Type":"application/json"
    },
    body:JSON.stringify({
      from,
      to:[clientEmail],
      subject:"TaxReady Books is calling you",
      html:
        "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto'>" +
        "<h2>TaxReady Books is calling you</h2>" +
        "<p>Hello " + escapeHtml(clientName || "Client") + ",</p>" +
        "<p>Your TaxReady Books bookkeeper has started a video call with you.</p>" +
        "<p><a href='" + escapeHtml(joinUrl) + "' style='display:inline-block;padding:12px 18px;background:#173f35;color:#fff;text-decoration:none;border-radius:8px'>Join Video Call</a></p>" +
        "</div>"
    })
  });

  const data = await response.json().catch(()=>({}));
  if (!response.ok) return res.status(response.status).json({success:false,error:data?.message || "Email could not be sent"});
  return res.status(200).json({success:true});
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}