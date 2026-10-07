const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 const [,,bg,out,scale]=process.argv;
 let html=fs.readFileSync(__dirname+'/back.html','utf8').replace('BG','file://'+bg);
 fs.writeFileSync(__dirname+'/tmp.html',html);
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1000,height:1491},deviceScaleFactor:parseFloat(scale||'1')});
 await p.goto('file://'+__dirname+'/tmp.html'); await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:out,clip:{x:0,y:0,width:1000,height:1491}});
 await b.close();
})();
