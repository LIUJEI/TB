const host = 'https://www.haigui.tv';
const headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": host + "/"
};

async function init(cfg) {}

const m = (s, r, i = 1) => (s.match(r) || [])[i] || "";
const fixPic = p => p && p.startsWith('/') ? host + p : p;

function getList(html) {
    return pdfa(html, ".module-item").map(it => {
        let id = m(it, /href="\/video\/(.*?)\/"/);
        let name = m(it, /title="(.*?)"/);
        if (!id || !name) return null;
        return {
            vod_id: id,
            vod_name: name,
            vod_pic: fixPic(m(it, /data-original="(.*?)"/) || m(it, /src="(.*?)"/)),
            vod_remarks: m(it, /module-item-note">(.*?)<\/div>/).replace(/<.*?>/g, "")
        };
    }).filter(Boolean);
}

async function home(filter) {
    const classes = [
        ["dianying","电影"],["dianshiju","电视剧"],["zongyi","综艺"],
        ["dongman","动漫"],["jilupian","纪录片"],["duanju","短剧"]
    ].map(([id,name]) => ({type_id:id,type_name:name}));

    const dict = {
        area: ["中国大陆","中国香港","中国台湾","美国","韩国","日本","泰国"],
        year: ["2025","2024","2023","2022","2021","2020"],
        lang: ["国语","英语","粤语","韩语","日语"]
    };

    const filters = {};
    classes.forEach(c => {
        filters[c.type_id] = [
            { key:"class", name:"类型", value:getSubClasses(c.type_id) },
            ...Object.keys(dict).map(k => ({
                key:k,
                name:{area:"地区",year:"年份",lang:"语言"}[k],
                value:[{n:"全部",v:""}].concat(dict[k].map(v=>({n:v,v})))
            }))
        ];
    });

    return JSON.stringify({ class: classes, filters });
}

function getSubClasses(tid) {
    const map = {
        dianying: [
            ["dongzuopian","动作片"],["xijupian","喜剧片"],
            ["aiqingpian","爱情片"],["kehuanpian","科幻片"],["kongbupian","恐怖片"]
        ],
        dianshiju: [
            ["guochanju","国产剧"],["gangtaiju","港台剧"],
            ["rihanju","日韩剧"],["oumeiju","欧美剧"]
        ]
    };
    return [{n:"全部",v:""}].concat((map[tid]||[]).map(([v,n])=>({n,v})));
}

async function homeVod() {
    const r = await req(host,{headers});
    return JSON.stringify({ list:getList(r.content) });
}

async function category(tid, pg, filter, extend={}) {
    let p = pg || 1;
    let id = extend.class || tid;
    let url = `${host}/filter/${id}`;
    ["area","lang","year"].forEach(k=>{
        if (extend[k]) url += `/${k}/${encodeURIComponent(extend[k])}`;
    });
    url += `/page/${p}/`;
    const r = await req(url,{headers});
    return JSON.stringify({ page:p, list:getList(r.content) });
}

async function detail(id) {
    const r = await req(`${host}/video/${id}/`,{headers});
    const h = r.content;

    const playFrom = pdfa(h,".module-tab-item")
        .map(it=>m(it,/<span>(.*?)<\/span>/)||"播放源")
        .join("$$$");

    const playUrl = pdfa(h,".module-player-list").map(l =>
        pdfa(l,".module-blocklist a").map(it=>{
            let pid = m(it,/href=\"\/play\/(.*?)\/\"/);
            if (!pid) return null;
            return `${m(it,/<span>(.*?)<\/span>/)||"正片"}$${pid}`;
        }).filter(Boolean).join("#")
    ).join("$$$");

    return JSON.stringify({
        list:[{
            vod_id:id,
            vod_name:m(h,/page-title\">(.*?)<\/h1>/),
            vod_pic:fixPic(m(h,/video-cover.*?data-src=\"(.*?)\"/)||m(h,/video-cover.*?src=\"(.*?)\"/)),
            type_name:(
                m(h,/tag-link[^>]*>[\s\S]*?icon-cate-[^<]*<\/i>\s*([^<\n]+)/) ||
                m(h,/icon-cate-[^<]*<\/i>\s*([^<\n]+)/)
            ).trim(),
            vod_year:m(h,/year\/(\d+)\//),
            vod_area:m(h,/area\/.*?\/ \">(.*?)\t/s).trim(),
            vod_director:m(h,/导演：<\/span>.*?<div.*?>(.*?)<\/div>/s).replace(/<.*?>|\//g,"").trim(),
            vod_actor:m(h,/主演：<\/span>.*?<div.*?>(.*?)<\/div>/s).replace(/<.*?>|\//g,"").trim(),
            vod_remarks:m(h,/备注：<\/span>.*?<div.*?>(.*?)<\/div>/),
            vod_content:m(h,/vod_content.*?<span>(.*?)<\/span>/s)||"【琉🔹芸❤广告勿信👉剧情】",
            vod_play_from:playFrom,
            vod_play_url:playUrl
        }]
    });
}

async function search(wd, quick, pg=1) {
    let url = `${host}/search/${encodeURIComponent(wd)}/${pg>1?`page/${pg}/`:""}`;
    const r = await req(url,{headers});
    const h = r.content;

    const items = pdfa(h,".module-search-item") || pdfa(h,".module-item");

    const list = items.map(it=>{
        let id = m(it,/\/video\/(.*?)\//);
        let name = m(it,/title=\"(.*?)\"/) || m(it,/alt=\"(.*?)\"/);
        if (!id || !name) return null;
        return {
            vod_id:id,
            vod_name:name,
            vod_pic:fixPic(m(it,/data-src=\"(.*?)\"/)||m(it,/data-original=\"(.*?)\"/)||m(it,/src=\"(.*?)\"/)),
            vod_remarks:m(it,/module-item-note\">(.*?)<\/div>/)||m(it,/video-serial\">(.*?)<\/span>/)
        };
    }).filter(Boolean);

    return JSON.stringify({ page:pg, list });
}

async function play(flag, id, flags) {
    const r = await req(`${host}/play/${id}/`,{headers});
    let u = m(r.content,/"url":"([^"]+\.m3u8[^"]*)"/);
    if (u) return JSON.stringify({ parse:0, url:u.replace(/\\/g,""), header:headers });
    return JSON.stringify({ parse:1, url:`${host}/play/${id}/`, header:headers });
}

export default { init, home, homeVod, category, detail, search, play };
