const https = require('https');

require('https').globalAgent.options.ca = require('ssl-root-cas/latest').create();

// https.get("https://dejt.jt.jus.br/cadernos/Diario_J_11.pdf",(err, res, body) => {
https.get("https://dejt.jt.jus.br/dejt/f/n/diariocon",(err, res, body) => {    
    
    let data = '';
    res.on('data', (chunk) => {
        data += chunk;
    });
    res.on('end', () => {
        console.log(JSON.parse(data).explanation);
    });
    console.log(JSON.stringify(body))
}).on("error", (err) => {
    console.log("Error: " + err.message);
});