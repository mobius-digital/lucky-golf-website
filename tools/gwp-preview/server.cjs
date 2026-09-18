const http=require('http'),fs=require('fs'),path=require('path');
const T={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp'};
http.createServer((q,s)=>{
  let f=q.url.split('?')[0]; if(f==='/')f='/index.html';
  const p=path.join(__dirname,f);
  if(!p.startsWith(__dirname)||!fs.existsSync(p)){s.writeHead(404);return s.end('nope')}
  s.writeHead(200,{'Content-Type':T[path.extname(p)]||'text/plain','Cache-Control':'no-store'});
  s.end(fs.readFileSync(p));
}).listen(4181,()=>console.log('harness on http://localhost:4181'));
