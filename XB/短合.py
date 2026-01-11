import 'assets://js/lib/crypto-js.js';
const UA = 'Mozilla/5.0 (Linux; Android 9; V2196A Build/PQ3A.190705.08211809; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:416;packageName:com.jp3.xg3';
const aggConfig = {
  keys: 'd3dGiJc651gSQ8w1',
  charMap: {
    '+': 'P', '/': 'X', '0': 'M', '1': 'U', '2': 'l', '3': 'E', '4': 'r', '5': 'Y', '6': 'W', '7': 'b', '8': 'd', '9': 'J',
    'A': '9', 'B': 's', 'C': 'a', 'D': 'I', 'E': '0', 'F': 'o', 'G': 'y', 'H': '_', 'I': 'H', 'J': 'G', 'K': 'i', 'L': 't',
    'M': 'g', 'N': 'N', 'O': 'A', 'P': '8', 'Q': 'F', 'R': 'k', 'S': '3', 'T': 'h', 'U': 'f', 'V': 'R', 'W': 'q', 'X': 'C',
    'Y': '4', 'Z': 'p', 'a': 'm', 'b': 'B', 'c': 'O', 'd': 'u', 'e': 'c', 'f': '6', 'g': 'K', 'h': 'x', 'i': '5', 'j': 'T',
    'k': '-', 'l': '2', 'm': 'z', 'n': 'S', 'o': 'Z', 'p': '1', 'q': 'V', 'r': 'v', 's': 'j', 't': 'Q', 'u': '7', 'v': 'D',
    'w': 'w', 'x': 'n', 'y': 'L', 'z': 'e'
  },
  headers: {
    default: { 'User-Agent': 'okhttp/3.12.11', 'content-type': 'application/json; charset=utf-8' }
  },
  platform: {
    百度: { host: 'https://api.jkyai.top', url1: '/API/bddjss.php?name=fyclass&page=fypage', url2: '/API/bddjss.php?id=fyid', search: '/API/bddjss.php?name=**&page=fypage' },
    锦鲤: { host: 'https://api.jinlidj.com', search: '/api/search', url2: '/api/detail' },
    番茄: { host: 'https://reading.snssdk.com', url1: '/reading/bookapi/bookmall/cell/change/v', url2: 'https://fqgo.52dns.cc/catalog', search: 'https://fqgo.52dns.cc/search' },
    星芽: { host: 'https://app.whjzjx.cn', url1: '/cloud/v2/theater/home_page?theater_class_id', url2: '/v2/theater_parent/detail', search: '/v3/search', loginUrl: 'https://u.shytkjgs.com/user/v1/account/login' },
    西饭: { host: 'https://xifan-api-cn.youlishipin.com', url1: '/xifan/drama/portalPage', url2: '/xifan/drama/getDuanjuInfo', search: '/xifan/search/getSearchList' },
    软鸭: { host: 'https://api.xingzhige.com', url1: '/API/playlet', search: '/API/playlet' },
    七猫: { host: 'https://api-store.qmplaylet.com', url1: '/api/v1/playlet/index', url2: 'https://api-read.qmplaylet.com/player/api/v1/playlet/info', search: '/api/v1/playlet/search' },
    围观: { host: 'https://api.drama.9ddm.com', url1: '/drama/home/shortVideoTags', url2: '/drama/home/shortVideoDetail', search: '/drama/home/search' },
    甜圈: { host: 'https://mov.cenguigui.cn', url1: '/duanju/api.php?classname', url2: '/duanju/api.php?book_id', search: '/duanju/api.php?name' }
  },
  platformList: [
    { name: '七猫短剧', id: '七猫' }, { name: '锦鲤短剧', id: '锦鲤' },{ name: '番茄短剧', id: '番茄' },
    { name: '星芽短剧', id: '星芽' }, { name: '西饭短剧', id: '西饭' },{ name: '软鸭短剧', id: '软鸭' },
    { name: '围观短剧', id: '围观' }, { name: '甜圈短剧', id: '甜圈' },{ name: '百度短剧', id: '百度' }
  ],
  search: { limit: 30, timeout: 6000 }
};

const ruleFilterDef = {
  百度: { area: '逆袭' },
  锦鲤: { area: '' },
  番茄: { area: 'videoseries_hot' },
  星芽: { area: '1' },
  西饭: { area: '' },
  软鸭: { area: '战神' },
  七猫: { area: '0' },
  围观: { area: '' },
  甜圈: { area: '推荐榜' }
};

const filterOptionsB64 = "eyLnlJzlnIgiOlt7ImtleSI6ImFyZWEiLCJuYW1lIjoi5Ymn5oOFIiwidmFsdWUiOlt7Im4iOiLlhajpg6giLCJ2IjoiIn0seyJuIjoi5o6o6I2Q5qacIiwidiI6IuaOqOiNkOamnCJ9LHsibiI6IueDreaSreamnCIsInYiOiLng63mkq3mppwifSx7Im4iOiLmlrDkuabmppwiLCJ2Ijoi5paw5Lmm5qacIn0seyJuIjoi5a6M57uT5qacIiwidiI6IuWujOe7k+amnCJ9LHsibiI6Iui/nui9veamnCIsInYiOiLov57ovb3mppwifSx7Im4iOiLlhY3otLnmppwiLCJ2Ijoi5YWN6LS55qacIn0seyJuIjoi5paw5YmnIiwidiI6IuaWsOWJpyJ9LHsibiI6IumAhuiirSIsInYiOiLpgIbooq0ifSx7Im4iOiLpnLjmgLsiLCJ2Ijoi6Zy45oC7In0seyJuIjoi546w5Luj6KiA5oOFIiwidiI6IueOsOS7o+iogOaDhSJ9LHsibiI6IuaJk+iEuOiZkOa4oyIsInYiOiLmiZPohLjomZDmuKMifSx7Im4iOiLosarpl6jmganmgKgiLCJ2Ijoi6LGq6Zeo5oGp5oCoIn0seyJuIjoi56We6LGqIiwidiI6IuelnuixqiJ9LHsibiI6IumprOeUsiIsInYiOiLpqaznlLIifSx7Im4iOiLpg73luILml6XluLgiLCJ2Ijoi6YO95biC5pel5bi4In0seyJuIjoi5oiY56We5b2S5p2lIiwidiI6IuaImOelnuW9kuadpSJ9LHsibiI6IuWwj+S6uueJqSIsInYiOiLlsI/kurrniakifSx7Im4iOiLlpbPmgKfmiJDplb8iLCJ2Ijoi5aWz5oCn5oiQ6ZW/In0seyJuIjoi5aSn5aWz5Li7IiwidiI6IuWkp+Wls+S4uyJ9LHsibiI6Iuepv+i2iiIsInYiOiLnqb/otooifSx7Im4iOiLpg73luILkv67ku5kiLCJ2Ijoi6YO95biC5L+u5LuZIn0seyJuIjoi5by66ICF5Zue5b2SIiwidiI6IuW8uuiAheWbnuW9kiJ9LHsibiI6IuS6suaDhSIsInYiOiLkurLmg4UifSx7Im4iOiLlj6Too4UiLCJ2Ijoi5Y+k6KOFIn0seyJuIjoi6YeN55SfIiwidiI6IumHjeeUnyJ9LHsibiI6IumXquWpmiIsInYiOiLpl6rlqZoifSx7Im4iOiLotZjlqb/pgIbooq0iLCJ2Ijoi6LWY5am/6YCG6KKtIn0seyJuIjoi6JmQ5oGLIiwidiI6IuiZkOaBiyJ9LHsibiI6Iui/veWmuyIsInYiOiLov73lprsifSx7Im4iOiLlpKnkuIvml6DmlYwiLCJ2Ijoi5aSp5LiL5peg5pWMIn0seyJuIjoi5a625bqt5Lym55CGIiwidiI6IuWutuW6reS8pueQhiJ9LHsibiI6IuiQjOWunSIsInYiOiLokIzlrp0ifSx7Im4iOiLlj6Tpo47mnYPosIsiLCJ2Ijoi5Y+k6aOO5p2D6LCLIn0seyJuIjoi6IGM5Zy6IiwidiI6IuiBjOWcuiJ9LHsibiI6IuWlh+W5u+iEkea0niIsInYiOiLlpYflubvohJHmtJ4ifSx7Im4iOiLlvILog70iLCJ2Ijoi5byC6IO9In0seyJuIjoi5peg5pWM56We5Yy7IiwidiI6IuaXoOaVjOelnuWMuyJ9LHsibiI6IuWPpOmjjuiogOaDhSIsInYiOiLlj6Tpo47oqIDmg4UifSx7Im4iOiLkvKDmib/op4nphpIiLCJ2Ijoi5Lyg5om/6KeJ6YaSIn0seyJuIjoi546w6KiA55Sc5a6gIiwidiI6IueOsOiogOeUnOWuoCJ9LHsibiI6IuWlh+W5u+eIseaDhSIsInYiOiLlpYflubvniLHmg4UifSx7Im4iOiLkuaHmnZEiLCJ2Ijoi5Lmh5p2RIn0seyJuIjoi5Y6G5Y+y5Y+k5LujIiwidiI6IuWOhuWPsuWPpOS7oyJ9LHsibiI6IueOi+WmgyIsInYiOiLnjovlpoMifSx7Im4iOiLpq5jmiYvkuIvlsbEiLCJ2Ijoi6auY5omL5LiL5bGxIn0seyJuIjoi5aix5LmQ5ZyIIiwidiI6IuWoseS5kOWciCJ9XX1dLCLplKbpsqQiOlt7ImtleSI6ImFyZWEiLCJuYW1lIjoi5YiG57G7IiwidmFsdWUiOlt7Im4iOiLlhajpg6giLCJ2IjoiIn0seyJuIjoi5oOF5oSf5YWz57O7IiwidiI6IjEifSx7Im4iOiLmiJDplb/pgIbooq0iLCJ2IjoiMiJ9LHsibiI6IuWlh+W5u+W8guiDvSIsInYiOiIzIn0seyJuIjoi5oiY5paX54Ot6KGAIiwidiI6IjQifSx7Im4iOiLkvKbnkIbnjrDlrp4iLCJ2IjoiNSJ9LHsibiI6IuaXtuepuuepv+i2iiIsInYiOiI2In0seyJuIjoi5p2D6LCL6Lqr5Lu9IiwidiI6IjcifV19XSwi55Wq6IyEIjpbeyJrZXkiOiJhcmVhIiwibmFtZSI6IuWIhuexuyIsInZhbHVlIjpbeyJuIjoi54Ot5YmnIiwidiI6InZpZGVvc2VyaWVzX2hvdCJ9LHsibiI6IuaWsOWJpyIsInYiOiJmaXJzdG9ubGluZXRpbWVfbmV3In0seyJuIjoi6YCG6KKtIiwidiI6ImNhdGVfNzM5In0seyJuIjoi5oC76KOBIiwidiI6ImNhdGVfMjkifSx7Im4iOiLnjrDoqIAiLCJ2IjoiY2F0ZV8zIn0seyJuIjoi5omT6IS4IiwidiI6ImNhdGVfMTA1MSJ9LHsibiI6IumprOeUsiIsInYiOiJjYXRlXzI2NiJ9LHsibiI6IuixqumXqCIsInYiOiJjYXRlXzEwNTMifSx7Im4iOiLpg73luIIiLCJ2IjoiY2F0ZV8yNjEifSx7Im4iOiLnpZ7osaoiLCJ2IjoiY2F0ZV8yMCJ9XX1dLCLmmJ/oir0iOlt7ImtleSI6ImFyZWEiLCJuYW1lIjoi5YiG57G7IiwidmFsdWUiOlt7Im4iOiLliaflnLoiLCJ2IjoiMSJ9LHsibiI6IueDreaSreWJpyIsInYiOiIyIn0seyJuIjoi5Lya5ZGY5LiT5LqrIiwidiI6IjgifSx7Im4iOiLmmJ/pgInlpb3liaciLCJ2IjoiNyJ9LHsibiI6IuaWsOWJpyIsInYiOiIzIn0seyJuIjoi6Ziz5YWJ5Ymn5Zy6IiwidiI6IjUifV19XSwi6KW/6aWtIjpbeyJrZXkiOiJhcmVhIiwibmFtZSI6IuWIhuexuyIsInZhbHVlIjpbeyJuIjoi5YWo6YOoIiwidiI6IiJ9LHsibiI6IumDveW4giIsInYiOiI2OEDpg73luIIifSx7Im4iOiLpnZLmmKUiLCJ2IjoiNjhA6Z2S5pilIn0seyJuIjoi546w5Luj6KiA5oOFIiwidiI6IjgxQOeOsOS7o+iogOaDhSJ9LHsibiI6IuixqumXqCIsInYiOiI4MUDosarpl6gifSx7Im4iOiLlpKflpbPkuLsiLCJ2IjoiODBA5aSn5aWz5Li7In0seyJuIjoi6YCG6KKtIiwidiI6Ijc5QOmAhuiirSJ9LHsibiI6IuaJk+iEuOiZkOa4oyIsInYiOiI3OUDmiZPohLjomZDmuKMifSx7Im4iOiLnqb/otooiLCJ2IjoiODFA56m/6LaKIn1dfV0sIui9r+m4rSI6W3sia2V5IjoiYXJlYSIsIm5hbWUiOiLliIbnsbsiLCJ2YWx1ZSI6W3sibiI6IuWFqOmDqCIsInYiOiIifSx7Im4iOiLmiJjnpZ4iLCJ2Ijoi5oiY56WeIn0seyJuIjoi6YCG6KKtIiwidiI6IumAhuiirSJ9LHsibiI6IumcuOaAuyIsInYiOiLpnLjmgLsifSx7Im4iOiLnpZ7osaoiLCJ2Ijoi56We6LGqIn0seyJuIjoi6YO95biCIiwidiI6IumDveW4giJ9LHsibiI6IueOhOW5uyIsInYiOiLnjoTlubsifSx7Im4iOiLoqIDmg4UiLCJ2Ijoi6KiA5oOFIn1dfV0sIuS4g+eMqyI6W3sia2V5IjoiYXJlYSIsIm5hbWUiOiLliIbnsbsiLCJ2YWx1ZSI6W3sibiI6IuWFqOmDqCIsInYiOiIifSx7Im4iOiLmjqjojZAiLCJ2IjoiMCJ9LHsibiI6IuaWsOWJpyIsInYiOiItMSJ9LHsibiI6IumDveW4guaDheaEnyIsInYiOiIxMjczIn0seyJuIjoi5Y+k6KOFIiwidiI6IjEyNzIifSx7Im4iOiLpg73luIIiLCJ2IjoiNTcxIn0seyJuIjoi546E5bm75LuZ5L6gIiwidiI6IjEyODYifSx7Im4iOiLlpYflubsiLCJ2IjoiNTcwIn0seyJuIjoi5Lmh5p2RIiwidiI6IjU5MCJ9LHsibiI6IuawkeWbvSIsInYiOiI1NzMifSx7Im4iOiLlubTku6MiLCJ2IjoiNTcyIn0seyJuIjoi6Z2S5pil5qCh5ZutIiwidiI6IjEyODgifSx7Im4iOiLmrabkvqAiLCJ2IjoiMzcxIn0seyJuIjoi56eR5bm7IiwidiI6IjU5NCJ9LHsibiI6Iuacq+S4liIsInYiOiI1NTYifSx7Im4iOiLkuozmrKHlhYMiLCJ2IjoiMTI4OSJ9LHsibiI6IumAhuiirSIsInYiOiI0MDAifSx7Im4iOiLnqb/otooiLCJ2IjoiMzczIn0seyJuIjoi5aSN5LuHIiwidiI6Ijc5NSJ9LHsibiI6Iuezu+e7nyIsInYiOiI3ODcifSx7Im4iOiLmnYPosIsiLCJ2IjoiNzkwIn0seyJuIjoi6YeN55SfIiwidiI6Ijc4NCJ9LHsibiI6IuWls+aAp+aIkOmVvyIsInYiOiIxMjk0In0seyJuIjoi5omT6IS46JmQ5rijIiwidiI6IjcxNiJ9LHsibiI6IumXquWpmiIsInYiOiI0ODAifSx7Im4iOiLlvLrogIXlm57lvZIiLCJ2IjoiNDAyIn0seyJuIjoi6L+95aa754Gr6JGs5Zy6IiwidiI6IjcxNSJ9LHsibiI6IuWutuW6rSIsInYiOiI2NzAifSx7Im4iOiLpqaznlLIiLCJ2IjoiNTU4In0seyJuIjoi6IGM5Zy6IiwidiI6IjcyNCJ9LHsibiI6IuWuq+aWlyIsInYiOiIzNDMifSx7Im4iOiLpq5jmiYvkuIvlsbEiLCJ2IjoiMTI5OSJ9LHsibiI6IuWoseS5kOaYjuaYnyIsInYiOiIxMjk1In0seyJuIjoi5byC6IO9IiwidiI6IjcyNyJ9LHsibiI6IuWuheaWlyIsInYiOiIzNDIifSx7Im4iOiLmm7/ouqsiLCJ2IjoiNzEyIn0seyJuIjoi56m/5LmmIiwidiI6IjMzOCJ9LHsibiI6IuWVhuaImCIsInYiOiI3MjMifSx7Im4iOiLnp43nlLDnu4/llYYiLCJ2IjoiMTI5MSJ9LHsibiI6IuS8pueQhiIsInYiOiIxMjkzIn0seyJuIjoi56S+5Lya6K+d6aKYIiwidiI6IjEyOTAifSx7Im4iOiLoh7Tlr4wiLCJ2IjoiNDkyIn0seyJuIjoi5YG35ZCs5b+D5aOwIiwidiI6IjEyNTgifSx7Im4iOiLohJHmtJ4iLCJ2IjoiNTI2In0seyJuIjoi6LGq6Zeo5oC76KOBIiwidiI6IjYyNCJ9LHsibiI6IuiQjOWunSIsInYiOiIzNTYifSx7Im4iOiLmiJjnpZ4iLCJ2IjoiNTI3In0seyJuIjoi55yf5YGH5Y2D6YeRIiwidiI6IjgxMiJ9LHsibiI6Iui1mOWpvyIsInYiOiIzNiJ9LHsibiI6IuelnuWMuyIsInYiOiIxMjY5In0seyJuIjoi56We6LGqIiwidiI6IjM3In0seyJuIjoi5bCP5Lq654mpIiwidiI6IjEyOTYifSx7Im4iOiLlm6LlrqAiLCJ2IjoiNTQ1In0seyJuIjoi5qyi5Zac5Yak5a62IiwidiI6IjQ2NCJ9LHsibiI6IuWls+W4nSIsInYiOiI2MTcifSx7Im4iOiLpk7blj5EiLCJ2IjoiMTI5NyJ9LHsibiI6IuWFteeOiyIsInYiOiIyOCJ9LHsibiI6IuiZkOaBiyIsInYiOiIxNiJ9LHsibiI6IueUnOWuoCIsInYiOiIyMSJ9LHsibiI6IuaCrOeWkSIsInYiOiIyNyJ9LHsibiI6IuaQnueskSIsInYiOiI3OTMifSx7Im4iOiLngbXlvIIiLCJ2IjoiMTI4NyJ9XX1dLCLnmb7luqYiOlt7ImtleSI6ImFyZWEiLCJuYW1lIjoi5YiG57G7IiwidmFsdWUiOlt7Im4iOiLpgIbooq0iLCJ2Ijoi6YCG6KKtIn0seyJuIjoi5oiY56WeIiwidiI6IuaImOelniJ9LHsibiI6IumDveW4giIsInYiOiLpg73luIIifSx7Im4iOiLnqb/otooiLCJ2Ijoi56m/6LaKIn0seyJuIjoi6YeN55SfIiwidiI6IumHjeeUnyJ9LHsibiI6IuWPpOijhSIsInYiOiLlj6Too4UifSx7Im4iOiLoqIDmg4UiLCJ2Ijoi6KiA5oOFIn0seyJuIjoi6JmQ5oGLIiwidiI6IuiZkOaBiyJ9LHsibiI6IueUnOWuoCIsInYiOiLnlJzlrqAifSx7Im4iOiLnpZ7ljLsiLCJ2Ijoi56We5Yy7In0seyJuIjoi6JCM5a6dIiwidiI6IuiQjOWunSJ9XX1dfQ==";

let xingya_headers = {};
function base64Encode(text) {
  return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(text));
}
function base64Decode(text) {
  return CryptoJS.enc.Utf8.stringify(CryptoJS.enc.Base64.parse(text));
}
async function request(url, options = {}) {
  const { method = 'GET', headers = {}, body, timeout = 5000 } = options;
  const isPost = method.toUpperCase() === 'POST';
  let requestBody = body && typeof body === 'object' ? JSON.stringify(body) : body;
  if (typeof req !== 'undefined') {
    return (await req(url, {
      method,
      headers: { ...aggConfig.headers.default, ...headers },
      body: isPost ? requestBody : null,
      timeout
    })).content;
  }
}
async function md5(str) {
  return CryptoJS.MD5(str).toString(CryptoJS.enc.Hex).toLowerCase();
}
function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}
function getFilterOptions() {
  try {
    return JSON.parse(base64Decode(filterOptionsB64));
  } catch (e) {
    console.error('filterOptions 解码失败', e);
    return {};
  }
}
async function getQmParamsAndSign() {
  const sessionId = Date.now().toString();
  const data = {
    "static_score": "0.8",
    "uuid": "00000000-7fc7-08dc-0000-000000000000",
    "device-id": "20250220125449b9b8cac84c2dd3d035c9052a2572f7dd0122edde3cc42a70",
    "sourceuid": "aa7de295aad621a6",
    "refresh-type": "0",
    "model": "22021211RC",
    "client-id": "aa7de295aad621a6",
    "brand": "Redmi",
    "sys-ver": "12",
    "phone-level": "H",
    "wlb-uid": "aa7de295aad621a6",
    "session-id": sessionId
  };
  const jsonStr = JSON.stringify(data);
  const base64Str = base64Encode(unescape(encodeURIComponent(jsonStr)));
  let qmParams = '';
  for (const c of base64Str) {
    qmParams += aggConfig.charMap[c] || c;
  }
  const paramsStr = `AUTHORIZATION=app-version=10001application-id=com.duoduo.readchannel=unknownis-white=net-env=5platform=androidqm-params=${qmParams}reg=${aggConfig.keys}`;
  const sign = await md5(paramsStr);
  return { qmParams, sign };
}
async function getHeaderX() {
  const { qmParams, sign } = await getQmParamsAndSign();
  return {
    'net-env': '5',
    'reg': '',
    'channel': 'unknown',
    'is-white': '',
    'platform': 'android',
    'application-id': 'com.duoduo.read',
    'authorization': '',
    'app-version': '10001',
    'user-agent': 'webviewversion/0',
    'qm-params': qmParams,
    'sign': sign
  };
}
async function init(cfg) {
  try {
    const res = JSON.parse(await request(aggConfig.platform.星芽.loginUrl, {
      method: 'POST',
      headers: { 'User-Agent': 'okhttp/4.10.0', platform: '1', 'Content-Type': 'application/json' },
      body: JSON.stringify({ device: '24250683a3bdb3f118dff25ba4b1cba1a' })
    }));
    const token = res?.data?.token || res?.token;
    xingya_headers = token ? { ...aggConfig.headers.default, authorization: token } : aggConfig.headers.default;
  } catch (e) {
    xingya_headers = aggConfig.headers.default;
  }
  return true;
}
async function getXingyaHeaders() {
  return xingya_headers.authorization ? xingya_headers : aggConfig.headers.default;
}
async function home(filter) {
  const classes = aggConfig.platformList.map(p => ({ type_name: p.name, type_id: p.id }));
  const filters = {};
  const filterOptions = getFilterOptions();
  aggConfig.platformList.forEach(item => {
    const platformId = item.id;
    if (filterOptions[platformId]) {
      filters[platformId] = filterOptions[platformId];
    }
  });
  return JSON.stringify({ class: classes, filters });
}
async function homeVod() { return await recommend(); }
async function recommend() {
  const randomPlat = aggConfig.platformList[Math.floor(Math.random() * aggConfig.platformList.length)];
  const platId = randomPlat.id;
  const area = ruleFilterDef[platId]?.area || '';
  const videos = await category(platId, 1, false, { area });
  const list = JSON.parse(videos).list.slice(0, 10).map(v => ({ ...v, vod_content: `${randomPlat.name} | ${v.vod_remarks}` }));
  return JSON.stringify({ list });
}
async function category(tid, pg, filter, extend) {
  const plat = aggConfig.platform[tid];
  const area = (extend?.area !== undefined ? extend.area : ruleFilterDef[tid]?.area) || '';
  const page = parseInt(pg) || 1;
  const videos = [];
  if (!plat) return JSON.stringify({ list: videos, page, pagecount: 1, limit: 0, total: 0 });
  try {
    if (tid === '七猫') {
      const sign = await md5(`operation=1playlet_privacy=1tag_id=${area}${aggConfig.keys}`);
      const url = `${plat.host}${plat.url1}?tag_id=${area}&playlet_privacy=1&operation=1&sign=${sign}`;
      const res = JSON.parse(await request(url, { headers: { ...await getHeaderX(), ...aggConfig.headers.default } }));
      (res?.data?.list || []).forEach(i => videos.push({
        vod_id: `七猫@${encodeURIComponent(i.playlet_id)}`,
        vod_name: i.title,
        vod_pic: i.image_link,
        vod_remarks: `${i.total_episode_num}集`
      }));
    } else if (tid === '百度') {
      const url = `${plat.host}${plat.url1.replace('fyclass', area).replace('fypage', page)}`;
      const res = JSON.parse(await request(url));
      if (res?.data) videos.push(...res.data.map(i => ({
        vod_id: `百度@${i.id}`, vod_name: i.title, vod_pic: i.cover, vod_remarks: `更新至${i.totalChapterNum}集`
      })));
    } else if (tid === '锦鲤') {
      const res = JSON.parse(await request(plat.host + plat.search, { method: 'POST', body: JSON.stringify({ page, limit: 24, type_id: area, keyword: '' }) }));
      if (res?.data?.list) videos.push(...res.data.list.map(i => ({
        vod_id: `锦鲤@${i.vod_id}`, vod_name: i.vod_name, vod_pic: i.vod_pic, vod_remarks: `${i.vod_total}集`
      })));
    } else if (tid === '番茄') {
      const sessionId = new Date().toISOString().slice(0, 16).replace(/-|T:/g, '');
      let url = `${plat.host}${plat.url1}?change_type=0&selected_items=${area}&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a&session_id=${sessionId}`;
      if (page > 1) url += `&offset=${(page - 1) * 12}`;
      const res = JSON.parse(await request(url));
      const items = res?.data?.cell_view?.cell_data || (Array.isArray(res?.data) ? res.data : []);
      items.forEach(i => {
        const v = i.video_data?.[0] || i;
        videos.push({ vod_id: `番茄@${v.series_id || v.book_id || ''}`, vod_name: v.title, vod_pic: v.cover || v.horiz_cover, vod_remarks: v.sub_title || '' });
      });
    } else if (tid === '星芽') {
      const headers = await getXingyaHeaders();
      const url = `${plat.host}${plat.url1}=${area}&type=1&class2_ids=0&page_num=${page}&page_size=24`;
      const res = JSON.parse(await request(url, { headers }));
      if (res?.data?.list) videos.push(...res.data.list.map(i => ({
        vod_id: `星芽@${plat.host}${plat.url2}?theater_parent_id=${i.theater.id}`,
        vod_name: i.theater.title, vod_pic: i.theater.cover_url, vod_remarks: `${i.theater.total}集`
      })));
    } else if (tid === '西饭') {
      const [typeId, typeName] = area.split('@');
      const ts = Math.floor(Date.now() / 1000);
      const url = `${plat.host}${plat.url1}?reqType=aggregationPage&offset=${(page - 1) * 30}&categoryId=${typeId}&quickEngineVersion=-1&scene=&categoryNames=${encodeURIComponent(typeName || '')}&categoryVersion=1&density=1.5&pageID=page_theater&version=2001001&androidVersionCode=28&requestId=${ts}aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTZjMWQ3NWI3ZDAiLCJpZCI6IjNiMzViZmYzYWE0OTgxNDQxNDBlZjI5N2JkMDY5NGNhIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;
      const res = JSON.parse(await request(url, { headers: aggConfig.headers.default }));
      const elements = res?.result?.elements || [];
      elements.forEach(s => (s.contents || []).forEach(v => {
        const d = v.duanjuVo;
        if (d) {
          videos.push({ vod_id: `西饭@${d.duanjuId}#${d.source}`, vod_name: d.title, vod_pic: d.coverImageUrl, vod_remarks: `${d.total}集` });
        }
      }));
    } else if (tid === '软鸭') {
      const url = `${plat.host}${plat.url1}/?keyword=${encodeURIComponent(area)}&page=${page}`;
      const res = JSON.parse(await request(url));
      if (res?.data) videos.push(...res.data.map(i => {
        const purl = `${i.title}@${i.cover}@${i.author}@${i.type}@${i.desc}@${i.book_id}`;
        return { vod_id: `软鸭@${encodeURIComponent(purl)}`, vod_name: i.title, vod_pic: i.cover, vod_remarks: i.type };
      }));
    } else if (tid === '围观') {
      const res = JSON.parse(await request(`${plat.host}${plat.search}`, {
        method: 'POST', body: JSON.stringify({ audience: "全部受众", page, pageSize: 30, searchWord: "", subject: "全部主题" })
      }));
      if (res?.data) videos.push(...res.data.map(i => ({
        vod_id: `围观@${i.oneId}`, vod_name: i.title, vod_pic: i.vertPoster, vod_remarks: `集数:${i.episodeCount} 播放:${i.viewCount}`
      })));
    } else if (tid === '甜圈') {
      const url = `${plat.host}${plat.url1}=${encodeURIComponent(area)}&offset=${page}`;
      const res = JSON.parse(await request(url));
      if (res?.data) {
        videos.push(...res.data.map(i => ({
          vod_id: `甜圈@${i.book_id}`,
          vod_name: i.title,
          vod_pic: i.cover,
          vod_remarks: `${i.sub_title || ''}`
        })));
      }
    }
  } catch (e) { }
  return JSON.stringify({ list: videos, page, pagecount: page + 1, limit: videos.length, total: videos.length * (page + 1) });
}
async function detail(id) {
  const [platId, ...rest] = id.split('@');
  const did = rest.join('@');
  const plat = aggConfig.platform[platId];
  if (!plat) return JSON.stringify({ list: [{ vod_id: id, vod_name: '平台不支持', vod_play_url: '' }] });
  let vod = { vod_id: id, vod_name: '未知', vod_pic: '', vod_remarks: '', vod_content: '', vod_play_from: '', vod_play_url: '' };
  try {
    if (platId === '七猫') {
      const didDecoded = decodeURIComponent(did);
      const sign = await md5(`playlet_id=${didDecoded}${aggConfig.keys}`);
      const url = `${plat.url2}?playlet_id=${didDecoded}&sign=${sign}`;
      const res = JSON.parse(await request(url, { headers: { ...await getHeaderX(), ...aggConfig.headers.default } }));
      if (res?.data) {
        const d = res.data;
        vod = {
          ...vod,
          vod_name: d.title,
          vod_pic: d.image_link,
          vod_remarks: `${d.total_episode_num}集`,
          vod_content: d.intro,
          vod_play_from: '💕琉芸👉七猫短剧',
          vod_play_url: (d.play_list || []).map(i => `${i.sort}$${i.video_url}`).join('#')
        };
      }
    } else if (platId === '百度') {
      const res = JSON.parse(await request(`${plat.host}${plat.url2.replace('fyid', did)}`));
      if (res) vod = { ...vod, vod_name: res.title, vod_pic: res.data?.[0]?.cover, vod_remarks: `更新至:${res.total || 0}集`, vod_play_from: '百度短剧', vod_play_url: (res.data || []).map(i => `${i.title}$${i.video_id}`).join('#') };
    } else if (platId === '锦鲤') {
      const res = JSON.parse(await request(`${plat.host}${plat.url2}/${did}`));
      if (res?.data) {
        const list = res.data;
        const urls = list.player ? Object.keys(list.player).map(k => `${k}$${list.player[k]}`) : [];
        vod = { ...vod, vod_name: list.vod_name, vod_pic: list.vod_pic, vod_remarks: list.vod_remarks, vod_play_from: '锦鲤短剧', vod_play_url: urls.join('#') };
      }
    } else if (platId === '番茄') {
      const res = JSON.parse(await request(`${plat.url2}?book_id=${did}`));
      if (res?.data) {
        const b = res.data.book_info;
        const u = (res.data.item_data_list || []).map(i => `${i.title}$${i.item_id}`).join('#');
        vod = { ...vod, vod_name: b.book_name, vod_pic: b.thumb_url, vod_remarks: `更新至${res.data.item_data_list?.length}集`, vod_play_from: '番茄短剧', vod_play_url: u };
      }
    } else if (platId === '星芽') {
      const headers = await getXingyaHeaders();
      const res = JSON.parse(await request(did, { headers }));
      if (res?.data) {
        const d = res.data;
        const u = (d.theaters || []).map(i => `${i.num}$${i.son_video_url}`).join('#');
        vod = { ...vod, vod_name: d.title, vod_pic: d.cover_url, vod_remarks: d.desc_tags + '', vod_play_from: '星芽短剧', vod_play_url: u };
      }
    } else if (platId === '西饭') {
      const [duanjuId, source] = did.split('#');
      const url = `${plat.host}${plat.url2}?duanjuId=${duanjuId}&source=${source}`;
      const res = JSON.parse(await request(url));
      if (res?.result) {
        const d = res.result;
        const u = (d.episodeList || []).map(e => `${e.index}$${e.playUrl}`).join('#');
        vod = { ...vod, vod_name: d.title, vod_pic: d.coverImageUrl, vod_remarks: d.updateStatus === 'over' ? `${d.total}集 已完结` : `更新${d.total}集`, vod_play_from: '西饭短剧', vod_play_url: u };
      }
    } else if (platId === '甜圈') {
      const url = `${plat.host}${plat.url2}=${did}`;
      const res = JSON.parse(await request(url));
      if (res) {
        const u = (res.data || []).map(item => `${item.title}$${item.video_id}`).join('#');
        vod = { ...vod, vod_name: res.book_name, vod_pic: res.book_pic, vod_remarks: `${res.duration || ''}`, vod_content: res.desc || '', vod_play_from: '甜圈短剧', vod_play_url: u };
      }
    } else if (platId === '软鸭') {
      const didDecoded = decodeURIComponent(did);
      const [title, img, author, type, desc, book_id] = didDecoded.split('@');
      const detailUrl = `${plat.host}${plat.url1}/?book_id=${book_id || did.split('@')[5]}`;
      const res = JSON.parse(await request(detailUrl, { headers: aggConfig.headers.default }));
      const u = (res.data?.video_list || []).map(e => `${e.title}$${e.video_id}`).join('#');
      vod = { ...vod, vod_name: title, vod_pic: img, vod_remarks: type, vod_content: desc, vod_play_from: '软鸭短剧', vod_play_url: u };
    } else if (platId === '围观') {
      const res = JSON.parse(await request(`${plat.host}${plat.url2}?oneId=${did}&page=1&pageSize=1000`));
      if (res?.data?.length) {
        const d = res.data;
        vod = { ...vod, vod_name: d[0].title, vod_pic: d[0].vertPoster, vod_remarks: `共${d.length}集`, vod_play_from: '围观短剧', vod_play_url: d.map(e => `${e.title}第${e.playOrder}集$${e.playSetting}`).join('#') };
      }
    }

  } catch (e) { vod.vod_name = '加载失败'; }
  return JSON.stringify({ list: [vod] });
}
async function play(flag, id) {
  if (/七猫/.test(flag)) {
    return JSON.stringify({ parse: 0, url: id });
  }
  if (/百度/.test(flag)) {
    const res = JSON.parse(await request(`https://api.jkyai.top/API/bddjss.php?video_id=${id}`));
    if (res?.data?.qualities) {
      const order = ["1080p", "sc", "sd"];
      const qMap = { "1080p": "蓝光", "sc": "超清", "sd": "标清" };
      const urls = [];
      order.forEach(k => {
        const q = res.data.qualities.find(x => x.quality === k);
        if (q) urls.push(qMap[k], q.download_url);
      });
      return JSON.stringify({ parse: 0, url: urls });
    }
  }
  if (/甜圈/.test(flag)) {
    return JSON.stringify({ parse: 0, url: `https://mov.cenguigui.cn/duanju/api.php?video_id=${id}&type=mp4` });
  }
  if (/锦鲤/.test(flag)) {
    try {
      const html = await request(`${id}&auto=1`, { headers: { referer: 'https://www.jinlidj.com/' } });
      const match = html.match(/let data\s*=\s*({[^;]*});/);
      if (match) {
        const data = JSON.parse(match[1]);
        if (data.url) return JSON.stringify({ parse: 0, url: data.url });
      }
    } catch {}
  }
  if (/番茄/.test(flag)) {
    try {
      const res = JSON.parse(await request(`https://fqgo.52dns.cc/video?item_ids=${id}`));
      if (res?.data?.[id]?.video_model) {
        const model = JSON.parse(res.data[id].video_model);
        const mainUrl = model?.video_list?.video_1?.main_url;
        if (mainUrl) return JSON.stringify({ parse: 0, url: base64Decode(mainUrl) });
      }
    } catch {}
  }
  if (/软鸭/.test(flag)) {
    const response = await request(`${aggConfig.platform.软鸭.host}/API/playlet/?video_id=${id}&quality=1080p`, { headers: aggConfig.headers.default });
    const res = JSON.parse(response);
    return JSON.stringify({ parse: 0, url: res.data?.video?.url || '' });
  }
  if (/围观/.test(flag)) {
    try {
      const ps = typeof id === 'string' ? JSON.parse(id) : id;
      const urls = [];
      if (ps?.super) urls.push("超清", ps.super);
      if (ps?.high) urls.push("高清", ps.high);
      if (ps?.normal) urls.push("流畅", ps.normal);
      return JSON.stringify({ parse: 0, url: urls });
    } catch { return JSON.stringify({ parse: 0, url: id }); }
  }
  return JSON.stringify({ parse: 0, url: id });
}
async function search(wd, quick, pg) {
  const page = parseInt(pg) || 1;
  const videos = [];
  try {
    const sign = await md5(`operation=2playlet_privacy=1search_word=${wd}${aggConfig.keys}`);
    const url = `${aggConfig.platform.七猫.host}${aggConfig.platform.七猫.search}?search_word=${encodeURIComponent(wd)}&playlet_privacy=1&operation=2&sign=${sign}`;
    const res = JSON.parse(await request(url, {
      headers: { ...await getHeaderX(), ...aggConfig.headers.default },
      timeout: aggConfig.search.timeout
    }));
    (res?.data?.list || []).forEach(i => {
      if (i.title.toLowerCase().includes(wd.toLowerCase())) {
        videos.push({
          vod_id: `七猫@${encodeURIComponent(i.playlet_id)}`,
          vod_name: i.title,
          vod_pic: i.image_link,
          vod_remarks: `七猫短剧｜${i.total_episode_num}集`
        });
      }
    });
  } catch {}
  const platforms = ['百度', '锦鲤', '番茄', '星芽', '西饭', '软鸭', '围观', '甜圈'];
  for (const tid of platforms) {
    const plat = aggConfig.platform[tid];
    try {
      let res, data;
      if (tid === '百度') {
        res = await request(`${plat.host}${plat.search.replace('**', encodeURIComponent(wd)).replace('fypage', page)}`);
        data = (JSON.parse(res)?.data || []).map(i => ({ vod_id: `百度@${i.id}`, vod_name: i.title, vod_pic: i.cover, vod_remarks: `百度短剧｜更新至${i.totalChapterNum}集` }));
      } else if (tid === '锦鲤') {
        res = await request(plat.host + plat.search, { method: 'POST', body: JSON.stringify({ page, limit: 30, keyword: wd }) });
        data = (JSON.parse(res)?.data?.list || []).map(i => ({ vod_id: `锦鲤@${i.vod_id}`, vod_name: i.vod_name, vod_pic: i.vod_pic, vod_remarks: `锦鲤短剧｜${i.vod_total}集` }));
      } else if (tid === '番茄') {
        res = await request(`${plat.search}?keyword=${encodeURIComponent(wd)}&page=${page}`);
        data = (JSON.parse(res)?.data || []).map(i => ({ vod_id: `番茄@${i.series_id}`, vod_name: i.title, vod_pic: i.cover, vod_remarks: `番茄短剧｜${i.sub_title}` }));
      } else if (tid === '星芽') {
        const headers = await getXingyaHeaders();
        res = await request(plat.host + plat.search, { method: 'POST', headers, body: JSON.stringify({ text: wd }) });
        data = (JSON.parse(res)?.data?.theater?.search_data || []).map(i => ({ vod_id: `星芽@${plat.host}${plat.url2}?theater_parent_id=${i.id}`, vod_name: i.title, vod_pic: i.cover_url, vod_remarks: `星芽短剧｜${i.total}集 播放:${i.play_amount_str}` }));
      } else if (tid === '西饭') {
        const ts = Math.floor(Date.now() / 1000);
        const url = `${plat.host}${plat.search}?reqType=search&offset=${(page - 1) * 30}&keyword=${encodeURIComponent(wd)}&quickEngineVersion=-1&scene=`;
        res = await request(url);
        data = (JSON.parse(res)?.result?.elements || []).map(vod => {
          const dj = vod.duanjuVo || {};
          return { vod_id: `西饭@${dj.duanjuId}#${dj.source}`, vod_name: dj.title, vod_pic: dj.coverImageUrl, vod_remarks: `西饭短剧｜${dj.total}集` };
        });
      } else if (tid === '软鸭') {
        res = await request(`${plat.host}${plat.search}/?keyword=${encodeURIComponent(wd)}&page=${page}`);
        data = (JSON.parse(res)?.data || []).map(i => {
          const purl = `${i.title}@${i.cover}@${i.author}@${i.type}@${i.desc}@${i.book_id}`;
          return { vod_id: `软鸭@${encodeURIComponent(purl)}`, vod_name: i.title, vod_pic: i.cover, vod_remarks: `软鸭短剧｜${i.type}` };
        });
      } else if (tid === '围观') {
        res = await request(`${plat.host}${plat.search}`, {
          method: 'POST',
          body: JSON.stringify({ audience: "", page, pageSize: 30, searchWord: wd, subject: "" })
        });
        data = (JSON.parse(res)?.data || []).map(i => ({ vod_id: `围观@${i.oneId}`, vod_name: i.title, vod_pic: i.vertPoster, vod_remarks: `围观短剧｜集数:${i.episodeCount} 播放:${i.viewCount}` }));
      } else if (tid === '甜圈') {
        const url = `${plat.host}${plat.search}=${encodeURIComponent(wd)}&offset=${page}`;
        res = await request(url);
        data = (JSON.parse(res)?.data || []).map(i => ({
          vod_id: `甜圈@${i.book_id}`,
          vod_name: i.title,
          vod_pic: i.cover,
          vod_remarks: `甜圈短剧｜${i.sub_title || '无简介'}`
        }));
      }
      if (data) videos.push(...data.filter(v => v.vod_name?.toLowerCase().includes(wd.toLowerCase())));
    } catch {}
  }
  return JSON.stringify({
    list: videos,
    page,
    pagecount: page + 1,
    limit: videos.length,
    total: videos.length * (page + 1)
  });
}
export function __jsEvalReturn() {
  return { init, home, homeVod, category, detail, play, proxy: null, search };
}
