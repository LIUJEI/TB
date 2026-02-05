/*
title: '星辰影院', author: '小可乐/v6.1.1'
说明：可以不写ext，也可以写ext，ext支持的参数和格式参数如下
"ext": {
    "host": "xxxx", //站点网址
    "timeout": 6000,  //请求超时，单位毫秒
    "catesSet": "电视剧&电影&综艺",  //指定分类和顺序
    "tabsSet": "土星&下载线1"  //指定线路和顺序
}
*/

const MOBILE_UA = 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36';
const DefHeader = {'User-Agent': MOBILE_UA};
var HOST;
var KParams = {
    headers: {'User-Agent': MOBILE_UA},
    timeout: 5000
};

async function init(cfg) {
    try {
        HOST = (cfg.ext?.host?.trim() || 'https://www.xcyycn.com').replace(/\/$/, '');
        KParams.headers['Referer'] = HOST;
        let parseTimeout = parseInt(cfg.ext?.timeout?.trim(), 10);
        if (parseTimeout > 0) {KParams.timeout = parseTimeout;}
        KParams.catesSet = cfg.ext?.catesSet?.trim() || '';
        KParams.tabsSet = cfg.ext?.tabsSet?.trim() || '';
        KParams.resHtml = await request(HOST);
    } catch (e) {
        console.error('初始化参数失败：', e.message);
    }
}

async function home(filter) {
    try {
        let resHtml = KParams.resHtml;
        if (!resHtml) {throw new Error('源码为空');}
        let typeArr = cutStr(resHtml, 'hl-nav-item£>', '</li>', '', false, 0, true).filter(flt => flt.includes('/v/'));
        let classes = typeArr.map((it,idx) => {
            let cName = cutStr(it, '>', '<', `分类${idx+1}`);
            let cId = cutStr(it, '/v/', '.', `值${idx+1}`);
            return {type_name: cName, type_id: cId};
        });
        if (KParams.catesSet) {classes = ctSet(classes, KParams.catesSet);}
        let filters = {};
        try {
            const nameObj = {class: 'class,剧情', area: 'area,地区', lang: 'lang,语言', year: 'year,年份', letter: 'letter,字母', by: 'by,排序'};
            const regObj = {class: /\d+---([^-]+)-/, area: /\/\d+-([^-]+)-/, lang: /\d+----([^-]+)-/, year: /-([^-]+)\./, letter: /\d+-----([^-]+)-/, by: /\d+--([^-]+)-/};
            let resHtmlList = await Promise.all(
                classes.map(async (it) => {
                    try {return await request(`${HOST}/vs/${it.type_id}-----------.html`);} catch (sErr) {return '';}
                })
            );
            classes.forEach((it,idx) => {
                let resfHtml = resHtmlList[idx];
                if (resfHtml) {
                    let flValArr = cutStr(resfHtml, 'hl-filter-list', '</ul>', '', false, 0, true).slice(1);
                    filters[it.type_id] = Object.entries(nameObj).map(([nObjk, nObjv]) => {
                        let [kkey, kname] = nObjv.split(',');
                        let tgVal = flValArr.find(fv => regObj[kkey].test(fv)) ?? '';
                        if (kkey === 'by') {tgVal = cutStr(resfHtml, 'hl-rb-title', '</div>', '', false);}
                        let tgValArr = cutStr(tgVal, '<a', '/a>', '', false, 0, true);
                        let tValArr = kkey !== 'by' ? tgValArr.slice(1) : tgValArr;                        
                        let kvalue = tValArr.map(el => {
                            let n = cutStr(el, '>', '<', '空白');
                            let v = n;
                            if (kkey === 'by') {v = el.match(regObj[kkey])?.[1] ?? '';}
                            return {n: n, v: v}; 
                        });
                        if (kkey !== 'by') {kvalue.unshift({n: '全部', v: ''});}
                        return {key: kkey, name: kname, value: kvalue};
                    }).filter(flt => flt.key && flt.value.length > 1);
                }
            });
        } catch (e) {
            filters = {}
        }
        return JSON.stringify({class: classes, filters: filters});
    } catch (e) {
        console.error('获取分类失败：', e.message);
        return JSON.stringify({class: [], filters: {}});
    }
}

async function homeVod() {
    try {
        let resHtml = KParams.resHtml;
        let VODS = getVodList(resHtml);
        return JSON.stringify({list: VODS});
    } catch (e) {
        console.error('推荐页获取失败：', e.message);
        return JSON.stringify({list: []});
    }
}

async function category(tid, pg, filter, extend) {
    try {
        pg = parseInt(pg, 10), pg = pg > 0 ? pg : 1;
        let fl = extend || {};
        let cateUrl = `${HOST}/vs/${fl.cateId || tid}-${fl.area ?? ''}-${fl.by ?? ''}-${fl.class ?? ''}-${fl.lang ?? ''}-${fl.letter ?? ''}---${pg}---${fl.year ?? ''}.html`;        
        let resHtml = await request(cateUrl);
        let VODS = getVodList(resHtml);
        let limit = VODS.length;
        let pagecount = cutStr(resHtml, 'hl-page-total£/', '页', '1');
        pagecount = Number(pagecount);
        return JSON.stringify({list: VODS, page: pg, pagecount: pagecount, limit: limit, total: limit*pagecount});
    } catch (e) {
        console.error('类别页获取失败：', e.message);
        return JSON.stringify({list: [], page: 1, pagecount: 0, limit: 30, total: 0});
    }
}

async function search(wd, quick, pg) {
    try {
        pg = parseInt(pg, 10), pg = pg > 0 ? pg : 1;
        let searchUrl = `${HOST}/s${wd}/page/${pg}.html`;
        let resHtml = await request(searchUrl);
        let VODS = getVodList(resHtml);
        return JSON.stringify({list: VODS, page: pg, pagecount: 10, limit: 30, total: 300});
    } catch (e) {
        console.error('搜索页获取失败：', e.message);
        return JSON.stringify({list: [], page: 1, pagecount: 0, limit: 30, total: 0});
    }
}

function getVodList(khtml) {
    try {
        if (!khtml) {throw new Error('源码为空');}  
        let kvods = [];
        let listArr = cutStr(khtml, 'hl-lazy', '</a>', '', false, 0, true).filter(flt => flt.includes('remarks'));
        for (let it of listArr) {
            let kname = cutStr(it, 'title="', '"', '名称');
            let kpic = cutStr(it, 'data-original="', '"', '图片');
            let kremarks = cutStr(it, 'remarks">', '</', '状态');
            let kid = cutStr(it, 'href="', '"');
            if (kid) {
                kvods.push({
                    vod_name: kname,
                    vod_pic: kpic,
                    vod_remarks: kremarks,
                    vod_id: `${kid}@${kname}@${kpic}@${kremarks}`
                });
            }
        }
        return kvods;
    } catch (e) {
        console.error(`生成视频列表失败：`, e.message);
        return [];
    }
}

async function detail(ids) {
    try {
        let [id, kname, kpic, kremarks] = ids.split('@');
        let detailUrl = !/^http/.test(id) ? `${HOST}${id}` : id;
        let resHtml = await request(detailUrl);
        if (!resHtml) {throw new Error('源码为空');}  
        let intros = cutStr(resHtml, '"clearfix">', '</ul>', '', false);
        let [ktabs, kurls] = [[], []];
        let zx_tabs = cutStr(resHtml, '<span class="hl-from', '/span>', '', false, 0, true).map((it,idx) => cutStr(it, '>', '<', `在线${idx+1}`) );
        ktabs.push(...zx_tabs);
        let zx_urls = cutStr(resHtml, 'hl-plays-list">', '</ul>', '', false, 0, true).map((item,idx) => cutStr(item, '<li', '</li>', '', false, 0, true).map(it => { return cutStr(it, '>', '</a>', 'noEpi')  + '$' + HOST + cutStr(it, 'href="', '"', 'noUrl'); }).join('#') );
        kurls.push(...zx_urls);
        let xzArr = cutStr(resHtml, 'hl-downs-list hl', '</ul>', '', false, 0, true);
        if (xzArr[0]) {
            xzArr.forEach((item,idx) => {
                let siglUrl = cutStr(item, 'down_url', '>', '', false, 0, true).map(it => `${cutStr(it, 'file_name="', '"', 'noEpi')}$${cutStr(it, 'value="', '"', 'noUrl')}` ).join('#');
                ktabs.push(`下载线${idx+1}`);
                kurls.push(siglUrl);
            });
        }
        if (KParams.tabsSet) {
            let ktus = ktabs.map((it, idx) => { return {type_name: it, type_value: kurls[idx]} });
            ktus = ctSet(ktus, KParams.tabsSet);
            ktabs = ktus.map(it => it.type_name);
            kurls = ktus.map(it => it.type_value);
        }
        let VOD = {
            vod_id: detailUrl,
            vod_name: kname,
            vod_pic: kpic,
            vod_remarks: kremarks,
            type_name: cutStr(intros, '类型：', '</li>', '类型'),
            vod_year: cutStr(intros, '年份：', '</li>', '1000'),
            vod_area: cutStr(intros, '地区：', '</li>', '地区'),
            vod_lang: cutStr(intros, '语言：', '</li>', '语言'),
            vod_director: cutStr(intros, '导演：', '</li>', '导演'),
            vod_actor: cutStr(intros, '主演：', '</li>', '主演'),
            vod_content: '【琉🔹芸❤广告勿信👉剧情】 '+cutStr(intros, '简介：', '</li>', kname),
            vod_play_from: ktabs.join('$$$💕琉芸👉'),
            vod_play_url: kurls.join('$$$')
        };
        return JSON.stringify({list: [VOD]});
    } catch (e) {
        console.error('详情页获取失败：', e.message);
        return JSON.stringify({list: []});
    }
}

async function play(flag, ids, flags) {
    try {
        let kp = 0, kurl = '';
        if (/下载/.test(flag)) {
            kurl = ids;
        } else {
            let resHtml = await request(ids);
            let codeObj = safeParseJSON(cutStr(resHtml, 'var player_£=', '<', '', false));       
            kurl = codeObj?.url ?? '';
            if (!/^http/.test(kurl)) {
                kurl = ids;
                kp = 1;
            }
        }
        return JSON.stringify({jx: 0, parse: kp, url: kurl, header: DefHeader});
    } catch (e) {
        console.error('播放失败：', e.message);
        return JSON.stringify({jx: 0, parse: 0, url: '', header: {}});
    }
}

function ctSet(kArr, setStr) {
    try {
        if (!Array.isArray(kArr) || kArr.length === 0 || typeof setStr !== 'string' || !setStr) { throw new Error('第一参数需为非空数组，第二参数需为非空字符串'); }
        const set_arr = [...kArr];
        const arrNames = setStr.split('&');
        const filtered_arr = arrNames.map(item => set_arr.find(it => it.type_name === item)).filter(Boolean);
        return filtered_arr.length? filtered_arr : [set_arr[0]];
    } catch (e) {
        console.error('ctSet 执行异常：', e.message);
        return kArr;
    }
}

function safeParseJSON(jStr){
    try {return JSON.parse(jStr);} catch(e) {return null;}
}

function cutStr(str, prefix = '', suffix = '', defVal = '', clean = true, i = 0, all = false) {
    try {
        if (typeof str !== 'string') {throw new Error('被截取对象必须为字符串');}
        const cleanStr = cs => String(cs).replace(/<[^>]*?>/g, ' ').replace(/(&nbsp;|[\u0020\u00A0\u3000\s])+/g, ' ').trim().replace(/\s+/g, ' ');
        const esc = s => String(s).replace(/[.*+?${}()|[\]\\/^]/g, '\\$&');
        let pre = esc(prefix).replace(/£/g, '[^]*?'), end = esc(suffix);
        const regex = new RegExp(`${pre || '^'}([^]*?)${end || '$'}`, 'g');
        const matchIter = str.matchAll(regex);
        if (all) {
            let matchArr = [...matchIter];
            if (!matchArr.length) {return [defVal];}
            return matchArr.map(ela => ela[1] !== undefined ? (clean ? cleanStr(ela[1]) : ela[1]) : defVal);
        }
        const idx = parseInt(i, 10);
        if (isNaN(idx)) {throw new Error('序号必须为整数');}
        let tgResult, matchIdx = 0;
        if (idx >= 0) {
            for (let elt of matchIter) {
                if (matchIdx++ === idx) {
                    tgResult = elt[1];
                    break;
                }
            }
        } else {
            let absI = Math.abs(idx), ringBuf = new Array(absI), ringPtr = 0, ringCnt = 0;
            for (let elt of matchIter) {
                ringBuf[ringPtr] = elt[1];
                ringPtr = (ringPtr + 1) % absI;
                ringCnt = Math.min(ringCnt + 1, absI);
                matchIdx++;
            }
            tgResult = (matchIdx >= absI && ringCnt > 0) ? ringBuf[ringPtr % ringCnt] : undefined;
        }
        return tgResult !== undefined ? (clean ? (cleanStr(tgResult) || defVal) : tgResult) : defVal;
    } catch (e) {
        console.error(`字符串截取错误：`, e.message);
        return all ? ['cutErr'] : 'cutErr';
    }
}

async function request(reqUrl, options = {}) {
    try {
        if (typeof reqUrl !== 'string' || !reqUrl.trim()) { throw new Error('reqUrl需为字符串且非空'); }
        if (typeof options !== 'object' || Array.isArray(options) || options === null) { throw new Error('options类型需为非null对象'); }
        options.method = options.method?.toUpperCase() || 'GET';
        if (['GET', 'HEAD'].includes(options.method)) {
            delete options.body;
            delete options.data;
            delete options.postType;
        }
        let {headers, timeout, ...restOpts} = options;
        const optObj = {
            headers: (typeof headers === 'object' && !Array.isArray(headers) && headers) ? headers : KParams.headers,
            timeout: parseInt(timeout, 10) > 0 ? parseInt(timeout, 10) : KParams.timeout,
            ...restOpts
        };
        const res = await req(reqUrl, optObj);
        if (options.withHeaders) {
            const resHeaders = typeof res.headers === 'object' && !Array.isArray(res.headers) && res.headers ? res.headers : {};
            const resWithHeaders = { ...resHeaders, body: res?.content ?? '' };
            return JSON.stringify(resWithHeaders);
        }
        return res?.content ?? '';
    } catch (e) {
        console.error(`${reqUrl}→请求失败：`, e.message);
        return options?.withHeaders ? JSON.stringify({ body: '' }) : '';
    }
}

export function __jsEvalReturn() {
    return {
        init,
        home,
        homeVod,
        category,
        search,
        detail,
        play,
        proxy: null
    };

}

