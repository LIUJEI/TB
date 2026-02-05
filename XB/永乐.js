let host = 'https://www.ylys.tv';
let headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": host + "/"
};

async function init(cfg) {}

/**
 * 通用解析：不做过滤，不做干扰
 */
function getList(html) {
    let videos = [];
    let items = pdfa(html, ".module-item,.module-card-item");
    items.forEach(it => {
        let idMatch = it.match(/detail\/(\d+)/);
        let nameMatch = it.match(/title="(.*?)"/) || it.match(/<strong>(.*?)<\/strong>/);
        let picMatch = it.match(/data-original="(.*?)"/) || it.match(/src="(.*?)"/);
        
        if (idMatch && nameMatch) {
            let pic = picMatch ? (picMatch[1] || picMatch[2]) : "";
            videos.push({
                "vod_id": idMatch[1],
                "vod_name": nameMatch[1].replace(/<.*?>/g, ""),
                "vod_pic": pic.startsWith('/') ? host + pic : pic,
                "vod_remarks": (it.match(/module-item-note">(.*?)<\/div>/) || ["",""])[1].replace(/<.*?>/g, "")
            });
        }
    });
    return videos;
}

async function home(filter) {
    return JSON.stringify({
        "class": [
            {"type_id":"1","type_name":"电影"},
            {"type_id":"2","type_name":"剧集"},
            {"type_id":"3","type_name":"综艺"},
            {"type_id":"4","type_name":"动漫"}
        ],
        "filters": {
            "1":[{"key":"class","name":"类型","value":[{"n":"全部","v":""},{"n":"动作片","v":"6"},{"n":"喜剧片","v":"7"},{"n":"爱情片","v":"8"},{"n":"科幻片","v":"9"},{"n":"恐怖片","v":"11"}]}],
            "2":[{"key":"class","name":"类型","value":[{"n":"全部","v":""},{"n":"国产剧","v":"13"},{"n":"港台剧","v":"14"},{"n":"日剧","v":"15"},{"n":"韩剧","v":"33"},{"n":"欧美剧","v":"16"}]}],
            "3":[{"key":"class","name":"类型","value":[{"n":"全部","v":""},{"n":"内地综艺","v":"27"},{"n":"港台综艺","v":"28"},{"n":"日本综艺","v":"29"},{"n":"韩国综艺","v":"36"}]}],
            "4":[{"key":"class","name":"类型","value":[{"n":"全部","v":""},{"n":"国产动漫","v":"31"},{"n":"日本动漫","v":"32"},{"n":"欧美动漫","v":"42"},{"n":"其他动漫","v":"43"}]}]
        }
    });
}

async function homeVod() {
    let resp = await req(host, { headers: headers });
    return JSON.stringify({ list: getList(resp.content) });
}

async function category(tid, pg, filter, extend) {
    let p = pg || 1;
    let targetId = (extend && extend.class) ? extend.class : tid;
    let url = host + "/vodtype/" + targetId + "/" + (parseInt(p) > 1 ? "page/" + p + "/" : "");
    let resp = await req(url, { headers: headers });
    return JSON.stringify({ 
        "list": getList(resp.content), 
        "page": parseInt(p) 
    });
}

async function detail(id) {
    let url = host + '/voddetail/' + id + '/';
    let resp = await req(url, { headers: headers });
    let html = resp.content;
    
    let playFrom = pdfa(html, ".module-tab-item").map(it => (it.match(/<span>(.*?)<\/span>/) || ["","线路"])[1]).join('$$$💕琉芸👉');
    let playUrl = pdfa(html, ".module-play-list-content").map(list => 
        pdfa(list, "a").map(a => {
            let n = (a.match(/<span>(.*?)<\/span>/) || ["","播放"])[1];
            let v = a.match(/href="\/play\/(.*?)\/"/);
            return n + '$' + (v ? v[1] : "");
        }).join('#')
    ).join('$$$');
    
    return JSON.stringify({
        list: [{
            'vod_id': id,
            'vod_name': (html.match(/<h1>(.*?)<\/h1>/) || ["", ""])[1],
            'vod_pic': (html.match(/data-original="(.*?)"/) || ["", ""])[1],
            'vod_content':(html.match(/introduction-content">.*?<p>(.*?)<\/p>/s) || ["", ""])[1].replace(/<.*?>/g, ""),
            'vod_play_from': playFrom,
            'vod_play_url': playUrl
        }]
    });
}

async function search(wd, quick, pg) {
    let p = pg || 1;
    let url = host + "/vodsearch/" + encodeURIComponent(wd) + "-------------/" + (parseInt(p) > 1 ? "page/" + p + "/" : "");
    let resp = await req(url, { headers: headers });
    return JSON.stringify({ list: getList(resp.content) });
}

async function play(flag, id, flags) {
    let url = host + "/play/" + id + "/";
    let resp = await req(url, { headers: headers });
    let m3u8 = resp.content.match(/"url":"([^"]+\.m3u8)"/);
    if (m3u8) return JSON.stringify({ parse: 0, url: m3u8[1].replace(/\\/g, ""), header: headers });
    return JSON.stringify({ parse: 1, url: url, header: headers });
}

export default { init, home, homeVod, category, detail, search, play };
