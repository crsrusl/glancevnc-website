#!/usr/bin/env python3
"""Generate GlanceVNC pages from shared templates and a route table."""

from pathlib import Path
from string import Template
import html
import json
import shutil
import xml.etree.ElementTree as ET
from discovery import write_llms
from guide_content import GUIDES, UPDATED, article

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
TEMPLATES = ROOT / "templates"
DOMAIN = "https://glancevnc.com"
APP_STORE_URL = "https://apps.apple.com/gb/app/glancevnc/id6768106616"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

# Each route defines its metadata, body template and structured data.
PAGES = {'/': {'title': 'GlanceVNC - VNC and RDP viewer for iPhone and iPad',
       'description': 'Connect to Mac, Windows and Linux desktops from iPhone or iPad with VNC, RDP and Mac '
                      'Screen Sharing. Use Apple Pencil, hardware keyboards and optional '
                      'certificate-verified TLS for compatible VNC servers.',
       'template': 'home.html',
       'social_description': 'Remote desktops for iPhone and iPad, with Apple Pencil pointer support, '
                             'hardware keyboards and optional certificate-verified TLS for compatible VNC '
                             'servers.',
       'structured_data': {'@context': 'https://schema.org',
                           '@type': 'MobileApplication',
                           '@id': 'https://glancevnc.com/#app',
                           'name': 'GlanceVNC',
                           'url': 'https://glancevnc.com/',
                           'applicationCategory': 'UtilitiesApplication',
                           'applicationSubCategory': 'VNC and RDP viewer',
                           'operatingSystem': ['iOS 18.0 or later', 'iPadOS 18.0 or later'],
                           'dateModified': '2026-11-05',
                           'softwareVersion': '1.7',
                           'downloadUrl': 'https://apps.apple.com/gb/app/glancevnc/id6768106616',
                           'description': 'GlanceVNC is a VNC and RDP viewer for iPhone and iPad running iOS '
                                          'or iPadOS 18 or later. It saves remote desktop connections, '
                                          'discovers nearby VNC servers, syncs profiles through private '
                                          'iCloud, and offers Touch and Trackpad controls, Apple Pencil '
                                          'pointer support on iPad, hardware keyboard shortcuts, plain-text '
                                          'clipboard exchange, per-connection display preferences, and '
                                          'optional certificate-verified TLS for compatible VNC servers. RDP '
                                          'uses TLS.',
                           'publisher': {'@type': 'Person',
                                         '@id': 'https://glancevnc.com/#developer',
                                         'name': 'Chris Russell'},
                           'softwareHelp': 'https://glancevnc.com/support.html',
                           'sameAs': 'https://apps.apple.com/gb/app/glancevnc/id6768106616',
                           'image': 'https://glancevnc.com/assets/social-preview.png',
                           'inLanguage': 'en-GB',
                           'isAccessibleForFree': False,
                           'author': {'@type': 'Person',
                                      '@id': 'https://glancevnc.com/#developer',
                                      'name': 'Chris Russell'}}},
 '/privacy.html': {'title': 'Privacy Policy - GlanceVNC',
                   'description': 'GlanceVNC privacy policy: what data is stored locally, what saved profile '
                                  'metadata can sync with private iCloud, how remote desktop credentials are '
                                  'protected, and how direct VNC and RDP connections work.',
                   'template': 'privacy.html',
                   'image_alt': 'GlanceVNC — Remote desktops at a glance. VNC viewer for iPhone and iPad.',
                   'structured_data': {'@context': 'https://schema.org',
                                       '@type': 'WebPage',
                                       '@id': 'https://glancevnc.com/privacy.html#webpage',
                                       'name': 'GlanceVNC Privacy Policy',
                                       'description': 'Privacy policy for GlanceVNC, including local '
                                                      'connection profile storage, private iCloud profile '
                                                      'sync, Keychain password storage, direct VNC and RDP '
                                                      'connections, nearby discovery, and data deletion.',
                                       'url': 'https://glancevnc.com/privacy.html',
                                       'inLanguage': 'en',
                                       'dateModified': '2026-11-05'}},
 '/support.html': {'title': 'Support - GlanceVNC',
                   'description': 'GlanceVNC setup and support for VNC, RDP and Mac Screen Sharing, '
                                  'including Apple Pencil, hardware keyboards, clipboard text, '
                                  'per-connection settings and certificate security.',
                   'template': 'support.html',
                   'section': 'support',
                   'image_alt': 'GlanceVNC — Remote desktops at a glance. VNC viewer for iPhone and iPad.',
                   'structured_data': {'@context': 'https://schema.org',
                                       '@type': 'FAQPage',
                                       '@id': 'https://glancevnc.com/support.html#faq',
                                       'url': 'https://glancevnc.com/support.html',
                                       'name': 'GlanceVNC Support FAQ',
                                       'description': 'Support answers for adding VNC and RDP connections, '
                                                      'Apple Pencil and hardware keyboard controls, '
                                                      'certificate security, Mac Screen Sharing, technical '
                                                      'compatibility and troubleshooting.',
                                       'inLanguage': 'en',
                                       'dateModified': '2026-11-05',
                                       'mainEntity': [{'@type': 'Question',
                                                       'name': 'Which devices can run GlanceVNC?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'GlanceVNC requires iOS 18 '
                                                                                  'or later on iPhone, or '
                                                                                  'iPadOS 18 or later on '
                                                                                  'iPad. Connect to a Mac, '
                                                                                  'Windows PC, Linux '
                                                                                  'computer or Raspberry Pi '
                                                                                  'running a compatible VNC '
                                                                                  'or RDP server, or Mac '
                                                                                  'Screen Sharing, that your '
                                                                                  'device can reach.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I add a VNC connection?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Open Saved Connections '
                                                                                  'and tap Add Connection. '
                                                                                  'Choose VNC, enter the '
                                                                                  'host or IP address and '
                                                                                  'port (usually 5900), then '
                                                                                  'choose the Operating '
                                                                                  'System and sign-in '
                                                                                  'method. Mac is the '
                                                                                  'default Operating System; '
                                                                                  'this choice also sets '
                                                                                  'remote keyboard '
                                                                                  'shortcuts. Set display, '
                                                                                  'pointer and VNC colour '
                                                                                  'preferences for this '
                                                                                  'connection before saving. '
                                                                                  'A vnc:// prefix is '
                                                                                  'accepted.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I add an RDP connection?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Open Saved Connections '
                                                                                  'and tap Add Connection. '
                                                                                  'Choose RDP, enter the '
                                                                                  'host or IP address and '
                                                                                  'port (3389 by default), '
                                                                                  'and add the remote '
                                                                                  'account username and '
                                                                                  'password. Choose Windows '
                                                                                  'or Linux under Operating '
                                                                                  'System so hardware '
                                                                                  'keyboard shortcuts use '
                                                                                  'Control. The remote '
                                                                                  'desktop needs a reachable '
                                                                                  'RDP server. Ordinary '
                                                                                  'usernames, user@domain '
                                                                                  'names and '
                                                                                  'DOMAIN\\username are '
                                                                                  'supported.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do RDP certificate approvals work?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'RDP uses TLS. If the '
                                                                                  'server certificate needs '
                                                                                  'approval, review and '
                                                                                  'trust it only after '
                                                                                  'checking that it belongs '
                                                                                  'to your computer. '
                                                                                  'Approval is remembered; a '
                                                                                  'changed certificate '
                                                                                  'requires a new review. '
                                                                                  'You can instead enable '
                                                                                  'Require certificate '
                                                                                  'security in Add or Edit '
                                                                                  'Connection to enforce '
                                                                                  'system trust, an imported '
                                                                                  'certificate or a SHA-256 '
                                                                                  'fingerprint. Strict '
                                                                                  'verification failures '
                                                                                  'block the connection '
                                                                                  'without an approval '
                                                                                  'override. To reset a '
                                                                                  'legacy approval, edit the '
                                                                                  'saved RDP connection and '
                                                                                  'choose Forget Trusted '
                                                                                  'Certificate.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Which RDP features are supported?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'RDP supports direct '
                                                                                  'TLS/NLA connections with '
                                                                                  'username/password '
                                                                                  'authentication, desktop '
                                                                                  'display, keyboard and '
                                                                                  'pointer input, scrolling '
                                                                                  'and plain-text clipboard '
                                                                                  'exchange. Where the '
                                                                                  'server supports it, '
                                                                                  'GlanceVNC requests a '
                                                                                  'landscape desktop size '
                                                                                  'matching the session '
                                                                                  'area. RDP gateways, '
                                                                                  'Kerberos or Azure '
                                                                                  'sign-in, audio, file or '
                                                                                  'device redirection are '
                                                                                  'not supported. Nearby '
                                                                                  'discovery finds VNC '
                                                                                  'services; add RDP '
                                                                                  'computers manually.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How does nearby discovery work?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'GlanceVNC finds Bonjour '
                                                                                  'VNC services advertised '
                                                                                  'as _rfb._tcp. on your '
                                                                                  'local network. Choose a '
                                                                                  'discovered desktop to '
                                                                                  'connect immediately after '
                                                                                  'entering its details, or '
                                                                                  'save it for later. Allow '
                                                                                  'Local Network access when '
                                                                                  'prompted. If discovery is '
                                                                                  'unavailable, check the '
                                                                                  'app’s Local Network '
                                                                                  'permission in system '
                                                                                  'Settings, or enter the '
                                                                                  'host and port manually.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Do saved connections and passwords sync '
                                                               'between devices?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Saved connection profiles '
                                                                                  'can sync through your '
                                                                                  'private iCloud database '
                                                                                  'when iCloud is available, '
                                                                                  'including the protocol '
                                                                                  'and optional certificate '
                                                                                  'security settings. '
                                                                                  'Passwords are stored '
                                                                                  'separately in Apple '
                                                                                  'Keychain and can sync '
                                                                                  'through iCloud Keychain '
                                                                                  'when enabled. The '
                                                                                  'Operating System choice, '
                                                                                  'per-connection session '
                                                                                  'preferences, desktop '
                                                                                  'thumbnails and custom '
                                                                                  'backgrounds stay on this '
                                                                                  'device.'}},
                                                      {'@type': 'Question',
                                                       'name': 'What sign-in method should I choose?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'For VNC, use Automatic '
                                                                                  'for most servers. Without '
                                                                                  'strict certificate '
                                                                                  'security, it can select '
                                                                                  'legacy Mac login when '
                                                                                  'offered or standard VNC '
                                                                                  'password authentication. '
                                                                                  'With Require certificate '
                                                                                  'security enabled on a '
                                                                                  'compatible VeNCrypt '
                                                                                  'server, Automatic selects '
                                                                                  'a supported X.509 mode. '
                                                                                  'Choose VNC password when '
                                                                                  'the server requires its '
                                                                                  'VNC viewer password. Mac '
                                                                                  'login requires a '
                                                                                  'compatible legacy Apple '
                                                                                  'Remote Desktop server and '
                                                                                  'cannot be combined with '
                                                                                  'strict VNC security.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How does certificate security work?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'In Add or Edit '
                                                                                  'Connection, enable '
                                                                                  'Require certificate '
                                                                                  'security in the Security '
                                                                                  'section. Choose system '
                                                                                  'trust, a public PEM or '
                                                                                  'DER certificate, or the '
                                                                                  'server’s SHA-256 '
                                                                                  'certificate fingerprint. '
                                                                                  'A mismatch, expired '
                                                                                  'certificate, failed TLS '
                                                                                  'handshake or unsupported '
                                                                                  'protocol blocks the '
                                                                                  'connection, including '
                                                                                  'reconnects. Secure VNC '
                                                                                  'requires a compatible '
                                                                                  'VeNCrypt 0.2 server with '
                                                                                  'an X.509 mode; standard '
                                                                                  'Mac Screen Sharing does '
                                                                                  'not support it. RDP '
                                                                                  'already uses TLS and can '
                                                                                  'also use this stricter '
                                                                                  'certificate check.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How does Apple Pencil work?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'On iPad, Apple Pencil '
                                                                                  'works automatically as a '
                                                                                  'direct remote pointer in '
                                                                                  'Touch or Trackpad mode. '
                                                                                  'Tap with the tip for a '
                                                                                  'left click; keep it down '
                                                                                  'and move to drag or draw. '
                                                                                  'Hover moves the cursor '
                                                                                  'without clicking on '
                                                                                  'supported iPads. Finger '
                                                                                  'navigation resumes when '
                                                                                  'the Pencil lifts. '
                                                                                  'Pressure, tilt, squeeze '
                                                                                  'and Pencil double-tap '
                                                                                  'actions are not part of '
                                                                                  'this pointer feature.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I connect to a Mac?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Enable Screen Sharing on '
                                                                                  'the Mac and the option '
                                                                                  'allowing VNC viewers to '
                                                                                  'control the screen with a '
                                                                                  'password. Add the Mac '
                                                                                  'host name or IP address, '
                                                                                  'leave Operating System '
                                                                                  'set to Mac, select VNC '
                                                                                  'password and enter that '
                                                                                  'VNC password. A Mac '
                                                                                  'account password is not '
                                                                                  'interchangeable with the '
                                                                                  'separately configured VNC '
                                                                                  'password. Standard Mac '
                                                                                  'Screen Sharing does not '
                                                                                  'offer the '
                                                                                  'certificate-backed '
                                                                                  'VeNCrypt mode used by the '
                                                                                  'optional strict VNC '
                                                                                  'security setting.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Why does my connection time out?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Check that your device '
                                                                                  'can reach the computer '
                                                                                  'over your local network '
                                                                                  'or through your own VPN, '
                                                                                  'that the selected VNC or '
                                                                                  'RDP server is running, '
                                                                                  'and that its host, port, '
                                                                                  'routing and firewall '
                                                                                  'settings are correct. '
                                                                                  'GlanceVNC connects '
                                                                                  'directly to your server '
                                                                                  'and does not provide a '
                                                                                  'remote-access relay.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Why does authentication fail?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Check the selected '
                                                                                  'protocol and saved '
                                                                                  'credentials. For RDP, use '
                                                                                  'the remote account '
                                                                                  'username and password. '
                                                                                  'For VNC, check the '
                                                                                  'sign-in method. Some Macs '
                                                                                  'offer newer Apple Screen '
                                                                                  'Sharing authentication '
                                                                                  'methods that GlanceVNC '
                                                                                  'does not support; '
                                                                                  'configure a VNC password. '
                                                                                  'For strict VNC security, '
                                                                                  'the server must support '
                                                                                  'VeNCrypt 0.2 with an '
                                                                                  'X.509 mode and the '
                                                                                  'configured certificate or '
                                                                                  'fingerprint must match.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I choose Touch or Trackpad mode?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'During a connection, open '
                                                                                  'the expanded toolbar, '
                                                                                  'choose Settings, then '
                                                                                  'Pointer mode. Touch '
                                                                                  'positions the pointer '
                                                                                  'where you tap and keeps '
                                                                                  'the zoomed view still. '
                                                                                  'Trackpad moves the '
                                                                                  'pointer relative to your '
                                                                                  'finger and follows it '
                                                                                  'when zoomed in. To set a '
                                                                                  'connection’s starting '
                                                                                  'mode, edit that '
                                                                                  'connection’s Session '
                                                                                  'Preferences. Switching '
                                                                                  'modes during a session '
                                                                                  'keeps your zoom level.'}},
                                                      {'@type': 'Question',
                                                       'name': 'What touch gestures are available?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Tap for a left click, '
                                                                                  'double-tap for a '
                                                                                  'double-click, use a '
                                                                                  'two-finger tap for a '
                                                                                  'right click, hold and '
                                                                                  'drag to move items, and '
                                                                                  'use two fingers to scroll '
                                                                                  'the remote computer. '
                                                                                  'Pinch zoom is always '
                                                                                  'available and changes '
                                                                                  'your local view, not the '
                                                                                  'computer’s screen '
                                                                                  'resolution. In Trackpad '
                                                                                  'mode, zoom centres on the '
                                                                                  'pointer and the view '
                                                                                  'follows it until the '
                                                                                  'desktop edge; in Touch '
                                                                                  'mode, pinch around an '
                                                                                  'area and tap the enlarged '
                                                                                  'content directly. For '
                                                                                  'gesture instructions '
                                                                                  'during a session, open '
                                                                                  'Settings and select How '
                                                                                  'to control your '
                                                                                  'computer.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I send keyboard input?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Tap the keyboard button '
                                                                                  'during a session to show '
                                                                                  'the on-screen keyboard; '
                                                                                  'it hides when a hardware '
                                                                                  'keyboard is attached. '
                                                                                  'Hardware keyboards work '
                                                                                  'immediately. '
                                                                                  'Command+C/X/A/Z and '
                                                                                  'Command+Shift+Z send '
                                                                                  'copy, cut, select all, '
                                                                                  'undo and redo. Command+V '
                                                                                  'transfers device '
                                                                                  'clipboard text and pastes '
                                                                                  'it remotely; '
                                                                                  'Command+Shift+V pastes '
                                                                                  'the existing remote '
                                                                                  'clipboard. The '
                                                                                  'connection’s Operating '
                                                                                  'System choice sends '
                                                                                  'remote Command for Mac '
                                                                                  'and Control for Windows '
                                                                                  'or Linux.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I choose colour depth?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'In Add or Edit '
                                                                                  'Connection, open Session '
                                                                                  'Preferences and choose '
                                                                                  '16-bit or 24-bit VNC '
                                                                                  'colour depth. The choice '
                                                                                  'is saved for that '
                                                                                  'connection on this device '
                                                                                  'and applies on the next '
                                                                                  'connection. RDP uses its '
                                                                                  'own colour handling.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Can I customise the home screen?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Open Settings and choose '
                                                                                  'Choose Background to pick '
                                                                                  'a photo; GlanceVNC stores '
                                                                                  'a resized copy on this '
                                                                                  'device. Use Default '
                                                                                  'Background removes it. '
                                                                                  'Saved connection cards '
                                                                                  'can show locally cached '
                                                                                  'desktop thumbnails; turn '
                                                                                  'off Show Connection '
                                                                                  'Thumbnails in Settings to '
                                                                                  'use placeholders '
                                                                                  'instead.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I close a remote session?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Tap the upward chevron to '
                                                                                  'show the session '
                                                                                  'controls, open Settings, '
                                                                                  'and choose Close '
                                                                                  'Connection. Confirm when '
                                                                                  'prompted.'}},
                                                      {'@type': 'Question',
                                                       'name': 'What VNC versions and authentication methods '
                                                               'are supported?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'GlanceVNC negotiates RFB '
                                                                                  '3.3, 3.7 and 3.8. It '
                                                                                  'supports no-password '
                                                                                  'servers, standard VNC '
                                                                                  'password authentication '
                                                                                  'and legacy Apple Remote '
                                                                                  'Desktop Mac login when '
                                                                                  'offered. Compatible '
                                                                                  'VeNCrypt 0.2 servers can '
                                                                                  'use certificate-verified '
                                                                                  'TLS with X509None, '
                                                                                  'X509Vnc or X509Plain. '
                                                                                  'Tight framebuffer '
                                                                                  'compression is supported; '
                                                                                  'Tight Security and '
                                                                                  'anonymous TLS are not.'}},
                                                      {'@type': 'Question',
                                                       'name': 'What framebuffer encodings are supported?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'The client supports Tight '
                                                                                  '(including JPEG data '
                                                                                  'within Tight), ZRLE, '
                                                                                  'CopyRect, Hextile and '
                                                                                  'Raw. It also supports '
                                                                                  'Zlib, which it advertises '
                                                                                  'for compatible macOS '
                                                                                  'Screen Sharing sessions. '
                                                                                  'H.264, Tight PNG, '
                                                                                  'standalone JPEG, RRE, '
                                                                                  'CoRRE and ZlibHex are not '
                                                                                  'supported.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Can GlanceVNC resize the remote desktop?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'GlanceVNC requests a '
                                                                                  'landscape desktop size '
                                                                                  'matching the session area '
                                                                                  'when the remote server '
                                                                                  'supports resizing. Mac '
                                                                                  'Screen Sharing retains '
                                                                                  'the Mac display '
                                                                                  'resolution. Choose Fit '
                                                                                  'whole desktop to see the '
                                                                                  'whole screen or Fill '
                                                                                  'screen to crop the edges '
                                                                                  'without stretching. Pinch '
                                                                                  'zoom enlarges only the '
                                                                                  'local view.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Does clipboard text work?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Version 1.3 supports '
                                                                                  'plain-text clipboard '
                                                                                  'exchange in compatible '
                                                                                  'VNC, Mac Screen Sharing '
                                                                                  'and RDP sessions. Tap the '
                                                                                  'upward chevron to show '
                                                                                  'the controls. Copy text '
                                                                                  'on the remote computer, '
                                                                                  'then tap Copy from remote '
                                                                                  'to copy it to your '
                                                                                  'device. Paste to remote '
                                                                                  'sends text from your '
                                                                                  'device clipboard to the '
                                                                                  'remote clipboard; approve '
                                                                                  'the iOS paste prompt if '
                                                                                  'asked, then use the '
                                                                                  'remote app’s Paste '
                                                                                  'command to insert it. '
                                                                                  'Images and files are not '
                                                                                  'supported.'}},
                                                      {'@type': 'Question',
                                                       'name': 'What happens while connecting or if a '
                                                               'connection fails?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'While connecting, '
                                                                                  'GlanceVNC shows a spinner '
                                                                                  'and the current stage. In '
                                                                                  'version 1.3, Mac Screen '
                                                                                  'Sharing waits up to 30 '
                                                                                  'seconds for the initial '
                                                                                  'desktop dimensions and '
                                                                                  'automatically retries '
                                                                                  'once if desktop '
                                                                                  'preparation times out. '
                                                                                  'RDP graphics setup is '
                                                                                  'more reliable, and the '
                                                                                  'app explains when no '
                                                                                  'desktop image arrives '
                                                                                  'within 15 seconds. If the '
                                                                                  'connection fails, the '
                                                                                  'panel explains why and '
                                                                                  'offers Reconnect. Use the '
                                                                                  'close button to return to '
                                                                                  'your saved connections. '
                                                                                  'You can select the error '
                                                                                  'message to copy it into a '
                                                                                  'support request.'}},
                                                      {'@type': 'Question',
                                                       'name': 'Where are What’s New, the privacy policy and '
                                                               'licence notices?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Open Settings from Saved '
                                                                                  'Connections, Nearby '
                                                                                  'Connections or the iPad '
                                                                                  'sidebar. What’s New shows '
                                                                                  'a text-based version '
                                                                                  'history, Privacy Policy '
                                                                                  'opens this website and '
                                                                                  'Third-party licences '
                                                                                  'shows the bundled notices '
                                                                                  'without an internet '
                                                                                  'connection.'}},
                                                      {'@type': 'Question',
                                                       'name': 'How do I report a support issue?',
                                                       'acceptedAnswer': {'@type': 'Answer',
                                                                          'text': 'Email '
                                                                                  'support@glancevnc.com '
                                                                                  'with your device model, '
                                                                                  'iOS or iPadOS version, '
                                                                                  'app version, connection '
                                                                                  'protocol, server type, '
                                                                                  'port, sign-in method and '
                                                                                  'error text. Include the '
                                                                                  'error message from a '
                                                                                  'failed connection, after '
                                                                                  'checking it for private '
                                                                                  'host names or addresses. '
                                                                                  'Do not send '
                                                                                  'passwords.'}}]}},
 '/guides/': {'title': 'Remote Desktop Setup Guides | GlanceVNC',
              'description': 'Practical GlanceVNC guides for connecting to your computers from iPad and '
                             'iPhone over a local network or your own VPN.',
              'template': 'guides.html',
              'section': 'guides',
              'stylesheets': ['/guides/guides.css?v=20261105'],
              'structured_data': {'@context': 'https://schema.org',
                                  '@type': 'CollectionPage',
                                  'name': 'Remote Desktop Setup Guides | GlanceVNC',
                                  'description': 'Practical GlanceVNC guides for connecting to your '
                                                 'computers from iPad and iPhone over a local network or '
                                                 'your own VPN.',
                                  'url': 'https://glancevnc.com/guides/',
                                  'inLanguage': 'en-GB'}},
 '/guides/mac-mini-ipad-vnc-tailscale/': {'title': 'Mac mini from iPad: VNC & Tailscale Setup | GlanceVNC',
                                          'description': 'Set up Mac Screen Sharing, connect from your iPad '
                                                         'with GlanceVNC, and use Tailscale for remote '
                                                         'access to your Mac mini.',
                                          'template': 'mac-mini-ipad.html',
                                          'section': 'guides',
                                          'structured_data': {'@context': 'https://schema.org',
                                                              '@type': 'TechArticle',
                                                              'name': 'Mac mini from iPad: VNC & Tailscale '
                                                                      'Setup | GlanceVNC',
                                                              'description': 'Set up Mac Screen Sharing, '
                                                                             'connect from your iPad with '
                                                                             'GlanceVNC, and use Tailscale '
                                                                             'for remote access to your Mac '
                                                                             'mini.',
                                                              'url': 'https://glancevnc.com/guides/mac-mini-ipad-vnc-tailscale/',
                                                              'inLanguage': 'en-GB',
                                                              'headline': 'Access your Mac mini from an iPad '
                                                                          'using VNC and Tailscale',
                                                              'datePublished': '2026-09-25',
                                                              'dateModified': '2026-11-05',
                                                              'author': {'@type': 'Person',
                                                                         'name': 'Chris Russell',
                                                                         'url': 'https://glancevnc.com/'},
                                                              'mainEntityOfPage': 'https://glancevnc.com/guides/mac-mini-ipad-vnc-tailscale/'}}}


# Guides are registered once for HTML, sitemap and the generated LLM reference.
for guide in GUIDES:
    route = '/guides/' + guide['slug'] + '/'
    PAGES[route] = {
        'title': guide['title'] + ' | GlanceVNC', 'description': guide['description'],
        'content': article(guide), 'section': 'guides',
        'structured_data': {
            '@context': 'https://schema.org', '@type': 'TechArticle',
            '@id': DOMAIN + route + '#article', 'url': DOMAIN + route,
            'headline': guide['title'], 'description': guide['description'],
            'datePublished': UPDATED, 'dateModified': UPDATED, 'inLanguage': 'en-GB',
            'author': {'@type': 'Person', '@id': DOMAIN + '/#developer', 'name': 'Chris Russell'},
            'mainEntityOfPage': DOMAIN + route,
        },
    }
PAGES['/guides/mac-mini-ipad-vnc-tailscale/']['structured_data']['dateModified'] = UPDATED
PAGES['/guides/']['structured_data']['mainEntity'] = {
    '@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'url': DOMAIN + route, 'name': page['title']}
        for i, (route, page) in enumerate(
            ((route, page) for route, page in PAGES.items() if route.startswith('/guides/') and route != '/guides/'), 1)
    ]
}


def header(section):
    return Template((TEMPLATES / "header.html").read_text()).substitute(
        guides_current=' aria-current="page"' if section == "guides" else "",
        support_current=' aria-current="page"' if section == "support" else "",
        app_store_url=html.escape(APP_STORE_URL, quote=True),
    )


def footer():
    return (TEMPLATES / "footer.html").read_text()


def render_page(route, page):
    metadata = {
        "title": page["title"],
        "description": page["description"],
        "social_description": page.get("social_description", page["description"]),
        "canonical": DOMAIN + route,
        "og_type": "article" if route.startswith("/guides/") and route != "/guides/" else "website",
        "image_alt": page.get("image_alt", "GlanceVNC app icon and remote desktop app description"),
    }
    schema = [page['structured_data']]
    if route != '/':
        crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN + '/'}]
        if route.startswith('/guides/') and route != '/guides/':
            crumbs.append({'@type': 'ListItem', 'position': 2, 'name': 'Guides', 'item': DOMAIN + '/guides/'})
        crumbs.append({'@type': 'ListItem', 'position': len(crumbs)+1, 'name': page['title'], 'item': DOMAIN + route})
        schema.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': crumbs})
    context = {key: html.escape(value, quote=True) for key, value in metadata.items()}
    context.update(
        header=header(page.get("section", "")),
        footer=footer(),
        content=page["content"] if "content" in page else (TEMPLATES / "pages" / page["template"]).read_text(),
        extra_stylesheets="\n".join(
            f'  <link rel="stylesheet" href="{html.escape(url, quote=True)}">'
            for url in page.get("stylesheets", [])
        ),
        structured_data=json.dumps(schema, ensure_ascii=False, indent=2).replace("</", "<\\/"),
    )
    return Template((TEMPLATES / "base.html").read_text()).substitute(context)


def copy_public(source, destination):
    """Copy public assets, omitting hidden files such as .DS_Store."""
    if source.name.startswith("."):
        return
    if source.is_dir():
        destination.mkdir(parents=True, exist_ok=True)
        for child in sorted(source.iterdir()):
            copy_public(child, destination / child.name)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build():
    # Resolve all templates before replacing the previous generated output.
    rendered = {route: render_page(route, page) for route, page in PAGES.items()}
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for route, content in rendered.items():
        target = OUT / route.lstrip("/")
        if route.endswith("/"):
            target /= "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    for name in ("styles.css", "assets", "guides/guides.css"):
        copy_public(ROOT / name, OUT / name)

    ET.register_namespace("", SITEMAP_NS)
    urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for route in PAGES:
        entry = ET.SubElement(urlset, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(entry, f"{{{SITEMAP_NS}}}loc").text = DOMAIN + route
    ET.indent(urlset, space="  ")
    (OUT / "sitemap.xml").write_bytes(
        ET.tostring(urlset, encoding="utf-8", xml_declaration=True) + b"\n"
    )
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    )
    write_llms(OUT, DOMAIN, PAGES, 'GlanceVNC')
    # Retain the historical root reference as a generated mirror, never a second source.
    (ROOT / 'llms.txt').write_text((OUT / 'llms.txt').read_text())
    print(f"Built {len(PAGES)} template pages, assets, sitemap.xml and robots.txt in {OUT}")


if __name__ == "__main__":
    build()
