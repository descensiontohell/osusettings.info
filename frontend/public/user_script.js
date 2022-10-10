let browser = "";
let user_data = {};

$(document).ready(function() {
  init();

})

function init() {
  browser = getBrowser();
  initJinja();
}
function getBrowser() {
  const ua = navigator.userAgent;
  if((ua.indexOf("Opera") || ua.indexOf('OPR')) != -1 ) return 'Opera';
  else if(ua.indexOf("Edg") != -1 ) return 'Edge';
  else if(ua.indexOf("Chrome") != -1 ) return 'Chrome';
  else if(ua.indexOf("Safari") != -1) return 'Safari';
  else if(ua.indexOf("Firefox") != -1 ) return 'Firefox';
  else if((ua.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) return 'IE';
  else return '';
}
function initJinja() {
  if (raw_data !== '{{ data | tojson | safe }}') { //TESTING PURPOSE ONLY
    user_data = JSON.parse(raw_data);
    console.log(user_data);
  }
  else {
    user_data = { isEmpty: true, player_name: 'NixX_Test' };
  }
}

/*
SERVER JUNK
*/

const api_path = "http://213.202.238.224:8080/api";

async function getDataAsync(path) {
  try {
    let response = await fetch(path);
    return await response.json();
  }
  catch(err){
    console.error(err);
    return { status: err };
  }
}
