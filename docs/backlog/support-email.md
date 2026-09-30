# Set up support@azulaudio.com

_Noted 2026-09-30. DONE 2026-09-30: Zoho Lite live (MX, SPF, DKIM selector zmail, DMARC p=none at Linode); inbound + outbound tested by owner; site footers + privacy page switched to support@. Moonbase: sending domain azulaudio.com verified (mb1/mb2 DKIM CNAMEs, return-path CNAME, shared DMARC), transactional sender support@azulaudio.com, fulfillment messages (Scatter, Transpose) and support email updated by owner; password-reset test email arrived from support@ (owner, 2026-09-30). Complete._
_ Decided 2026-09-30: Zoho Mail Lite (paid, ~$1/user/month: real mailbox + IMAP, so support@ can also be added to the Gmail/Apple Mail app and send as support@). Owner adds DNS at Linode by hand.
No noreply@: Moonbase can't set a reply-to, so its transactional sender should be support@ (replies reach support).
Once support@ works, also replace the Gmail address on the privacy page (`privacy/index.html`, 2 places)._

azulaudio.com has no email today (no MX or TXT records at Linode DNS), so customer contact points
at the owner's personal Gmail. Replace it with `support@azulaudio.com`.

## To do
- [ ] Pick a provider: forwarding only (e.g. Cloudflare Email Routing, ImprovMX) or a real mailbox
      (Google Workspace, Fastmail, Zoho). Forwarding is free but can't send *as* support@ without extra setup.
- [ ] Add the provider's MX + SPF (TXT) records, plus DKIM/DMARC if sending, in Linode DNS for
      azulaudio.com. These don't touch the A/CNAME records GitHub Pages uses.
- [ ] Replace the Gmail address everywhere it appears:
  - Site footer "Contact" link: `index.html`, `scatter/index.html`, `transpose/index.html`
  - Moonbase fulfillment messages: Scatter, Transpose ("Need help? Email ...")
  - Moonbase support/reply-to address; optionally a custom email sending domain
    (https://help.moonbase.sh/en/articles/9845316-custom-email-sending-domains-and-addresses)
- [ ] Send a test to support@ and reply from it.
