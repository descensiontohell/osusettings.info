let players = [];
let reader;
let mouse_pos;
let hover_header = "";
let hover_row = "";
let hover_cell = "";
let hover_index = -1;
let avatar_timer;
let avatar_id;
let avatar_visible = false;
let typing_timer;
let scroll_timer;
let search_string = "";
let selected_filter = -1;
let forced_search = true; //when false, double checks if search string is different from returned list because keyup process is sometimes interrupted
const column = { //how columns are addressed(string), sized(px), and how it addresses the object(func)
//column object: must match the player object:
  //locked: column can't be removed in options
  //string: how columns are addressed in the header
  //size: object for the header size, accepts min, default, and max variables
  //func(): how the list displays the data for the object variable in player
  //long(): how the profile displays the data for the object variable in player
  rank: {
    locked: true,
    string: "Rank",
    size:{ min:30, max:40 },
    func:function(x){ return '#' + (x.rank + 1) }},
  global_rank: {
    string: "Global",
    size:{ min:30, default:40, max:75 },
    func:function(x){ return (chkNull(x.global_rank) && x.is_active) ? '#'+x.global_rank : ""}},
  performance: {
    locked: true,
    string: "PP",
    string_long: "Performance Points",
    size:{ min:32, default:38, max:38 },
    func:function(x){ return x.performance }},
  username: {
    locked: true,
    string: "Username",
    size:{ min:75, default:122, max:250 },
    func:function(x){ return linkProfile(x) }},
  playstyle: {
    locked: true,
    string: "Playstyle",
    size:{ min:55, default:65, max:100 },
    func:function(x){ return " "+recolorPlaystyle(strNull(x.playstyle)) }},
  mouse_edpi: {
    string: "eDPI",
    string_long: "Effective DPI at x1080 Resolution",
    size:{ min:36, default:54, max:64 },
    func:function(x){ return strNull(x.mouse_edpi, "eDPI") }},
  dpi: {
    string: "DPI",
    size:{ min:36, default:44, max:52 },
    func:function(x){ return strNull(x.dpi, "dpi") }},
  os_sens: {
    string: "OS Sens",
    string_long: "Operating System Sensitivity",
    size:{ min:50, default:55, max:65 },
    func:function(x){ return recolorOS(x) },
    long:function(x){ return recolorOS(x, true) }},
  multiplier: {
    string: "osu! Sens",
    string_long: "osu! Sensitivity",
    size:{ min:28, default:64, max:64 },
    func:function(x){ return strNull(x.multiplier, "x") }},
  osu_res:{
    string: "osu! Res",
    string_long: "osu! Resolution",
    size:{ min:61, default:65, max:75 },
    func:function(x){ return chkNull(x.res_width) ? x.res_width+"x"+x.res_height : "" }}, //res_width res_height
  hz: {
    string: "Monitor Hz",
    string_long: "Monitor Refresh Rate",
    size:{ min:28, default:65, max:65 },
    func:function(x){ return strNull(x.hz, "Hz") }},
  raw_input: {
    string: "Raw",
    string_long: "osu! Raw Input",
    size:{ min:25, max:25 },
    func:function(x){ return chkNull(x.raw_input) ? (x.raw_input ? "On" : "Off") : "" }},
  polling: {
    string: "Polling",
    string_long: "Mouse Polling Rate",
    size:{ min:37, max:37 },
    func:function(x){ return strNull(x.polling, "hz") }},
  play_area: {
    string: "Play Area",
    string_long: "Estimated Range of Movement",
    size:{ min:62, default:80, max:100 },
    func:function(x){ return strNull(x.play_area, "mm\u00B2") }},
  mouse: {
    string: "Mouse Model",
    size:{ min:80, default:176, max:250 },
    id: "mouse",
    func: function(x){ return strNull(x.mouse.name) },
    sensor: {
      string: "Sensor",
      string_long: "Mouse Sensor",
      size:{ min:91, default:105, max:200 },
      func:function(x){ return strNull(x.mouse.sensor) }},
    weight: {
      string: "Weight",
      string_long: "Mouse Weight",
      size:{ min:25, default:42, max:42 },
      func:function(x){ return strNull(x.mouse.weight, "g") }},
      /*
    length: {
      string: "Length",
      size:{ min:25, default:41, max:41 },
      func:function(x){ return strNull(x.mouse.length, "mm") }},
    width: {
      string: "Width",
      size:{ min:25, default:35, max:35 },
      func:function(x){ return strNull(x.mouse.width, "mm") }},
    height: {
      string: "Height",
      size:{ min:25, default:39, max:39 },
      func:function(x){ return strNull(x.mouse.height, "mm") }},
      */
    lwh: {
      string: "Mouse L x W x H",
      string_long: "Length x Width x Height of Mouse",
      size:{ min:70, default:101, max:200},
      func: function(x){ return chkNull(x.mouse.length) ? `${x.mouse.length}x${x.mouse.width}x${x.mouse.height}mm\u00B3` : "" },
      long: function(x){ return chkNull(x.mouse.length) ? `${x.mouse.length}mm x ${x.mouse.width}mm x ${x.mouse.height}mm` : "? x ? x ?" }},
    switch: {
      string: "Mouse Sw.",
      string_long: "Mouse Switch",
      size:{ min:50, default:105, max:125 },
      func:function(x){ return strNull(x.mouse.switch) }}},
  mousepad: {
    string: "Mousepad",
    size:{ min:80, default:125, max:250 },
    func:function(x){ return strNull(x.mousepad.name) }},
  keyboard: { //subject to change
    string: "Keyboard Model",
    size:{ min:80, default:154, max:250 },
    func:function(x){ return strNull(x.keyboard.name) }},
  keyboard_switch: {
    string: "KB Switch",
    string_long: "Keyboard Switch",
    size:{ min:83, default:100, max:150 },
    func:function(x){ return strNull(x.switch.name) }},
  updated: {
    string: "Last Update",
    string_long: "Date of Latest Edit",
    size:{ min:36, default:72, max:100 },
    func:function(x){ return strNull(x.last_updated) }},
}
function sizeStr(index, obj) { //takes column._.size
  if (obj == {}) return "<div>";
  let str = obj.min ? `min-width:${obj.min}px;` : "";
  str += obj.max ? `max-width:${obj.max}px;` : "";
  if (obj.current > 0) str += `width:${obj.current}px;`;
  else str += obj.default ? `width:${obj.default}px;` : "";
  return `<div id='headr${index}' style='${str}'>`;
}
function chkNull(s) {
  if (s !== null || typeof str !== 'undefined') return true; //undefined check shouldn't be necessary
  else return false;
}
function strNull(str, post_str = "", replace_str = "") {
  if (str === null || typeof str === 'undefined') return replace_str; //undefined check shouldn't be necessary
  else return str+post_str;
}
function strEmpty(str, post_str = "") {
  if (str === "") return "?";
  else return str+post_str;
}
const headers = [ column.rank, column.global_rank, column.performance, column.username, column.playstyle, column.mouse_edpi, column.dpi, column.multiplier,
  column.os_sens, column.osu_res, column.hz, column.raw_input, column.play_area, column.mouse, column.mousepad, column.mouse.sensor, column.mouse.lwh,
  column.keyboard, column.keyboard_switch, column.updated ];
const default_layout = [ 0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19 ];
let locked_layout;
let layout = default_layout;

/*
HTML EVENT LISTENER SHIT
*/

$(document).ready(function() {
  loadHeaderOptions();
  refreshHeaders();
  getNewList();
  $("#column_apply_button").click(function() {
    applyColumns();
  });
  $("#column_default_button").click(function() {
    defaultColumns();
  });
  $('.tab').hover(function(e){
    $('#'+e.target.closest('div[class=tab]').id).stop(true, false).animate({ top: "-2px" }, 250);
    }, function(e) {
    $('#'+e.target.closest('div[class=tab]').id).stop(true, false).animate({ top: "-80px" }, 250);
  });
  $("#list").mouseover(function(e) {
    if (e.target.closest('td')) {
      if (hover_row !== e.target.closest('tr').id) {
        hover_row = e.target.closest('tr').id;
        hover_index = parseIndex(hover_row);
        miniProfile();
      }
      if (hover_cell !== e.target.closest('td').id) {
        hover_cell = e.target.closest('td').id;
        noteHandler();
      }
    }
  });
  $('#list').mouseenter(function(e) {
    headerHandler('list');
  });
  $("#top_container").mouseenter(function(e) {
    headerHandler('main');
  });
  $("#headers").mouseenter(function(e) {
    headerHandler('headers');
  });
  $("#note_container").hover(function(e) {
    $('#note_container').addClass('hidden');
  });
  $("#headers").mouseover(function(e) {
    if (e.target.closest('div').id !== hover_header) { //this mouse event shit is a fucking mess
      hover_header = e.target.closest('div').id;
      headerNameHandler(hover_header);
    }
  });
  $("#headers").click(function(e) {
    if (e.target.closest('a')) {
      //when a header is clicked and not resized
      let id = e.target.closest('div').id;
      console.log('#'+id+' click');
    }
    else if (e.target.closest('div').id != 'table_container') {
      let id = e.target.closest('div').id;
      let index = parseIndex(id);
      //console.log($('#headers').children()[index].children[0]); //this target works
      console.log(`#${id} resize ${$('#'+id).children()[0].clientWidth}px`);
    }
  });
  $('#applied_filters').click(function(e) {
    if (e.target.closest('a')) {
      let filter = e.target.closest('div').id;
      if (selected_filter > -1) highlightSelect(false, `#filtr${selected_filter}`);
      selected_filter = parseIndex(filter);
      highlightSelect(true, `#${filter}`)
      $('#filter_delete_button').prop('disabled', false);
    }
  });
  $('#filter_delete_button').click(function(e) {
    removeFilter(selected_filter);
  });
  $('#filter_reset_button').click(function(e) {
    removeFilter();
  });
  // optional method to allow live search
  $('#search_text').click(function(e){
    forced_search = false;
  });
  $('#search_text').keyup(function(){
    const s = chkNameSearch();
    if (typeof s === 'string') {
      typing_timer = setTimeout(startNameSearch, 750, s);
    }
  });
  $(document).scroll(function() {
    chkScroll();
  });
})

function parseIndex(s) { //ids 5 chars + int
  s = s.substring(5);
  let id = parseInt(s);
  return id;
}

function loadHeaderOptions() {
  let cb_string = "";
  locked_layout = [];
  for (let i = 0; i < headers.length; i++) {
    if (!headers[i].locked) {
      let label = `'header_cb${i}'`;
      let checked = layout.includes(i) ? " checked" : "";
      //let locked = headers[i].locked ? " disabled='disabled'" : "";
      cb_string += `<input type='checkbox' id=${label}`+/*${locked}*/`${checked}><label for=${label}>${headers[i].string}</label><br>`;
    }
    else locked_layout.push(i);
  }
  $("#applied_columns").html(cb_string);
}
function applyColumns() {
  let selected = $('#applied_columns').children('input:checked');
  layout = new Int8Array(locked_layout.length+selected.length);
  let i = 0;
  for (i; i < locked_layout.length; i++) layout[i] = locked_layout[i];
  for (let j = 0; j < selected.length; j++) {
    layout[i] = parseInt(selected[j].id.substring(9));
    i++;
  }
  layout = layout.sort();
  refreshLayout();
}
function defaultColumns() {
  let j = 0;
  for (let i = 0; i < headers.length; i++) {
    if (default_layout[j] == i) {
      if (!headers[i].locked) $(`#header_cb${i}`)[0].checked = true;
      j++;
    }
    else $(`#header_cb${i}`)[0].checked = false;
  }
  layout = default_layout;
  refreshLayout();
}
function refreshLayout() {
  for (let i = 0; i < pages.length; i++) addPage(i, true);
  refreshAll();
}

function removeFilter(index = -1) {
  if (index > -1) api_filters[index].set("");
  else {
    for (index = 0; index < api_filters.length; index++) api_filters[index].set("");
  }
  getNewList();
}

function highlightSelect(highlight, element) {
  $(element).removeClass();
  if (highlight) {
    $(element).addClass('clk_div_selected');
  }
  else $(element).addClass('clk_div');
}

function chkScroll() {
  let obj = $(document)[0].scrollingElement;
  clearTimeout(scroll_timer);
  if (obj.scrollHeight - obj.scrollTop - obj.clientHeight < 1 && !page_limit) {
    getNewPage();
  }
  else {
    scroll_timer = setTimeout(chkPage, 150);
  }
}
function chkPage() {
  let calc = calcPage();
  if (calc != page_current) {
    page_current = calc;
    refreshList(calc);
  } 
}

function linkProfile(player) {
  let flag = getCountryFlag(player);
  let color = player.is_active ? "" : "style='color:#a1a1a1' ";
  //return `<a ${color}href='https://osu.ppy.sh/u/${player.osu_id}' onclick='linkOnClick()'>${player.name}</a> ${flag}`;
  return `<a ${color}onclick='return osuUserClick("${player.osu_id}")' href='https://osu.ppy.sh/u/${player.osu_id}' target='_blank'>${player.name}</a> ${flag}`;
}
function osuUserClick(id){
  return linkOnClick(`https://osu.ppy.sh/u/${id}`);
}
function linkOnClick(url) {
  /* code to add parameter in history when using a link instead of opening a new tab
  const url = window.location.href.split('?')[0];
  let params = new URLSearchParams(window.location.search);
  params.set('backed', true);
  window.history.replaceState(null, null, `${url}?${params.toString()}`);*/
  if (navigator.userAgent.indexOf('Safari') >= 0) {
    return true;
  }
  else {
    window.open(url,'_blank');
    return false;
  }
}

function getCountryFlag(player, small = true) {
  let file;
  let flag;
  if (!player.country) file = '1f3f4-200d-2620-fe0f';
  else {
    let chars = player.country.split('')
      .map(char =>  127397 + char.charCodeAt());
    file = `${chars[0].toString(16)}-${chars[1].toString(16)}`;
  }
  if (small) flag = "flag_small";
  else flag = "flag_medium";
  return `<div class="${flag}" style="background-image: url('https://twemoji.maxcdn.com/v/14.0.2/svg/${file}.svg')"></div>`;
}

function recolor(s, color) {
  return `<span style='color:${color}'>${s}</span>`;
}

function recolorPlaystyle(s) { //probably temporary shit, maybe not
  let color;
  switch(s) {
    case ("Mouse/KB"):
      color = "#80c8ff";
      break;
    case ("Mouse Only"):
      color = "#ffacc7";
      break;
    case ("Hybrid"):
      color = "#92ff8e";
      break;
    case ("Click/X"):
    case ("rClick/Z"):
      color = "#daa5fd";
      break;
    default:
      color = "#ffffff";
      break;
  }
  return recolor(s, color);
}

function recolorOS(player, long = false) {
  let accel = false;
  let str1;
  if (long) {
    str1 = `OS: ${strNull(player.os_sens, "/11", "?")}&emsp;Accel: `;
  }
  else str1 = strNull(player.os_sens, "/11 ");
  let str2;
  if (!chkNull(player.os_accel)) {
    str2 = long ? "?" : "";
  }
  else if (!player.os_accel) str2 = "Off";
  else {
    str2 = "On";
    accel = true;
  }
  if (player.raw_input) return recolor(str1+str2, "#a1a1a1");
  else if (accel) return str1 + recolor(str2, "#f00a0a");
  else return str1+str2;
}

function noteHandler() {
  if (hover_cell.length < 5) {
    $("#note_container").addClass('hidden');
    return;
  }
  let player = players[parseIndex(hover_cell)];
  switch (hover_cell.substring(0,5)) {
    case ('mouse'): //monkaS all this mess just to place the stupid note
      if (column.mouse.func(player) === "") {
        $("#note_container").addClass('hidden');
        return;
      }
      let pos = $('#'+hover_cell).position();
      let scrollTop = $(document)[0].scrollingElement.scrollTop;
      let scrollLeft = $(document)[0].scrollingElement.scrollLeft;
      let margin = $('#top_container')[0].clientHeight;  //should probably be a constant
      let header = $('#headers').children()[0].clientHeight;
      $("#note_container").html(mouseProfile(player));
      let pos_max = $(window).outerHeight() - $('#note_container')[0].clientHeight;
      let x = pos.left - $("#note_container").width() - scrollLeft - 6; //warning: arbitrary number
      let y = pos.top - scrollTop + margin;
      if (x < 0) x = pos.left + $('#'+hover_cell).width() - scrollLeft + 18; //warning: arbitrary number
      if (y > pos_max - 12) y = pos_max - 14; //12 is scrollbar width, should probably be a constant
      else if (y < margin + header) y = margin + header;
      $("#note_container").css('left', x); 
      $("#note_container").css('top', y);
      break;
  }
  $("#note_container").removeClass('hidden');
}

function headerHandler(mouseover) {
  $('#main_container').addClass('hidden');
  $('#profile_container').addClass('hidden');
  $('#header_container').addClass('hidden');
  switch (mouseover) {
    case 'main':
      resetHoverVars();
      $("#note_container").addClass('hidden');
      $('#main_container').removeClass('hidden');
      break;
    case 'headers':
      resetHoverVars();
      $("#note_container").addClass('hidden');
      $('#header_container').removeClass('hidden');
      break;
    case 'list':
      if (!forced_search) forceNameSearch();
      $('#profile_container').removeClass('hidden');
      break;
  }
}
function resetHoverVars() {
  $("#avatar_container").css('display','none');
  avatar_visible = false;
  hover_header = "";
  hover_row = "";
  hover_cell = "";
  hover_index = -1;
}

function headerNameHandler(id) {
  if (id.substring(0,5) === 'headr') {
    let s = headers[layout[parseIndex(id)]].string;
    $('#header_name').removeClass();
    if (s.length > 15) {
      $('#header_name').addClass('header_name_smaller');
    }
    else if (s.length > 10) {
      $('#header_name').addClass('header_name_small');
    }
    else {
      $('#header_name').addClass('header_name_normal');
    }
    $('#header_name').html(`[${s}]`);
  }
}

function miniProfile() {
  player = players[hover_index];
  avatarTimeout(player.osu_id);
  $("#username_container").html(`${player.name} ${getCountryFlag(player, false)}`); //add country flag
  let str_rank = `${column.global_rank.func(player)}&emsp;${column.performance.func(player)}pp<br></span>`;
  $("#settings_rank").html(str_rank);
  $("#settings_container_left").html(mouseSensSettings(player));
  $("#settings_container_right").html(peripheralSettings(player));
}

function mouseProfile(player) {
  let str = `<span style='font-size:12'>${column.mouse.func(player)}</span><br>`;
  str += `${strNull(player.mouse.weight,"g","?")}, ${column.mouse.lwh.long(player)}`;
  str += `<div style='text-align:left'>Sensor: ${strNull(player.mouse.sensor,"","?")}<br>Switches: ${strNull(player.mouse.switch,"","?")}</div>`;
  return str;
}

function avatarTimeout(id) {
  clearTimeout(avatar_timer);
  if (avatar_visible) avatarFadeOut();
  avatar_timer = setTimeout(function() {
    $("#avatar_container").attr("src", "https://a.ppy.sh/" + id);
    avatar_id = id;
  }, 250);
}

function avatarFadeOut() {
  avatar_visible = false;
  $("#avatar_container").fadeOut(250);
}
function avatarFadeIn() {
  $("#avatar_container").fadeIn(250, function() { avatar_visible = true; });
}

function mouseSensSettings(player) {
  let str = `<span style='font-size:16'>${column.playstyle.func(player)}<br></span>`;
  str += `${strNull(player.dpi,"","?")} DPI @ ${strEmpty(column.osu_res.func(player))}, ${strEmpty(column.hz.func(player))} Hz<br>`;
  str += `eDPI @ x1080: ${strNull(player.mouse_edpi, "", "?")} eDPI<br>`;
  str += `Raw Input: ${strEmpty(column.raw_input.func(player))}&emsp;${column.os_sens.long(player)}<br>`;
  return str;
}

function peripheralSettings(player) {
  let str = `<span style='font-size:10'>Mouse:<br></span>&emsp;${strEmpty(column.mouse.func(player))}`; //add switch for tablet later
  str += `<span style='font-size:10'><br>Mousepad:<br></span>&emsp;${strEmpty(column.mousepad.func(player))}`;
  str += `<span style='font-size:10'><br>Keyboard:<br></span>&emsp;${strEmpty(column.keyboard.func(player))}<br>&emsp;${strEmpty(column.keyboard_switch.func(player))} Switches`;
  return str;
}

function startNameSearch(str) {
  search_string = str;
  console.log("searching for "+str);
  api_params.name = str;
  getNewList();
}
function chkNameSearch() {
  clearTimeout(typing_timer);
  const s = $('#search_text').val();
  if (s !== search_string) {
    return s;
  }
  return false;
}
function forceNameSearch() {
  let s = chkNameSearch();
  if (typeof s === 'string') startNameSearch(s);
  forced_search = true;
}

/*
SERVER JUNK
*/

let new_page_queue = false;
let loaded_page = 0;
const pages = []; //each page ~32kb max
let page_last = 0; //amount of rows on last page
let page_limit = 0; //if last page is reached
let page_current = 0;
const page_size = 50;
const api_path = "http://213.202.238.224:8080/api/";
const api_params = {
  is_mouse: "true", //bool NECESSARY
  order_by: "pp", //'-pp', 'edpi', '-edpi'
  max_rank: "", //int, 10k max and default
  playstyle: "", //int
  name: "", //search string
  min_edpi: "", //int
  max_edpi: "", //int
  mouse: "", //search string
  mousepad: "", //search string
  keyboard: "", //search string
  country: "", //country code string, how tf am i gonna do this
  page: 1, //int, page 1 default
}
const api_filters = [ //there's probably a cleaner way to do this
  { name: 'Username',
    get: ()=> { return api_params.name }, 
    string: function() { return `"${this.get()}"` },
    set: (x)=> {
      api_params.name = x;
      if (x === "") $('#search_text').val(""); } },
  { name: 'Playstyle',
    get: ()=> { return api_params.playstyle },
    string: function() { return `"${this.get()}"` }, //change later
    set: (x)=> { api_params.playstyle = x } },
  { name: 'Minimum eDPI',
    get: ()=> { return api_params.min_edpi },
    string: function() { return  `${this.get()} eDPI Min.` },
    set: (x)=> { api_params.min_edpi = x } },
  { name: 'Maximum eDPI',
    get: ()=> { return api_params.max_edpi },
    string: function() { return  `${this.get()} eDPI Max.` },
    set: (x)=> { api_params.max_edpi = x } },
  { name: 'Mouse', get: ()=> { return api_params.mouse},
    string: function() { return `"${this.get()}"` },
    set: (x)=> { api_params.mouse = x } },
  { name: 'Mousepad',
    get: ()=> { return api_params.mousepad },
    string: function() { return `"${this.get()}"` },
    set: (x)=> { api_params.mousepad = x } },
  { name: 'Keyboard',
    get: ()=> { return api_params.keyboard },
    string: function() { return `"${this.get()}"` },
    set: (x)=> { api_params.keyboard = x } },
  { name: 'Country',
    get: ()=> { return api_params.country },
    string: function() { return `"${this.get()}"` }, //change later
    set: (x)=> { api_params.country = x } },
];
function chkFilter(obj) {
  if (obj.get() === "") return false;
  else return true
}
function updateFilterList() {
  let str = "";
  for (let i = 0; i < api_filters.length; i++) {
    if (chkFilter(api_filters[i])) str += `<a><div id='filtr${i}' class='clk_div'>&emsp;${api_filters[i].name}:<br>${api_filters[i].string()}</div><br></a>`;
  }
  if (str === "") {
    $('#filter_reset_button').prop('disabled', true);
    str = "<span style='color: gray'>&emsp;[none]</span>";
  }
  else $('#filter_reset_button').prop('disabled', false);
  $('#applied_filters').html(str);
  $('#filter_delete_button').prop('disabled', true);
  selected_filter = -1;
}

function setApiPlaystyle(arr) {
  let s = "";
  for (let i = 0; i < arr.length; i++) {
    if (i == 0) s = arr[i];
    else s += `&playstyle=${arr[i]}`;
  }
  api_params.playstyle = s;
}

function getApiUrl() {
  let s = api_path + 'players?';
  for (const [key, value] of Object.entries(api_params)) {
    if (value) s += `${key}=${value}&`;
  }
  return s.slice(0, -1);
}

async function getNewList() {
  new_page_queue = true;
  loaded_page = 0;
  api_params.page = "";
  $("#list").html("");
  setLoadMsg();
  let response = await getDataAsync(getApiUrl());
  if (response.status === 'ok') {
    page_last = 0;
    page_limit = false;
    players = response.data.players;
    for (let i = 0; i < players.length; i++) initPlayer(i);
    page_last = players.length;
    if (players.length < page_size) {
      page_limit = true;
    }
    addPage();
    refreshList();
    loaded_page = 1;
  }
  new_page_queue = false;
  setLoadMsg(response.status);
  updateFilterList();
}

async function getNewPage() {
  if (new_page_queue || page_limit) {
    refreshList(loaded_page - 1);
    return;
  }
  setLoadMsg();
  api_params.page = loaded_page + 1;
  let response = await getDataAsync(getApiUrl());
  if (response.status === 'ok') {
    let length = response.data.players.length;
    if (length > 0) {
      page_last = length;
      let index = loaded_page * page_size;
      for (let i = 0; i < length; i++) {
        players.push(response.data.players[i]);
        initPlayer(i+index);
      }
      if (length < page_size) {
        page_limit = true;
      }
      addPage(loaded_page);
      refreshList(); 
    }
  }
  setLoadMsg(response.status);
}

function initPlayer(index) {
  players[index].rank = index;
  if (players[index].mouse_edpi) {
    let x = Math.round(36576 / players[index].mouse_edpi);
    let y = Math.round(27432 / players[index].mouse_edpi);
    players[index].play_area = `${x}x${y}`;
  }
}

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

function setLoadMsg(str = '') {
  let str2;
  switch (str) {
    case '':
      $('#loading_text').html("Loading...");
      $('#loading_text').removeClass('hidden');
      break;
    case 'ok':
      $('#loading_text').addClass('hidden');
      break;
    case 'bad_request':
      str2 = getApiUrl().substring(api_path.length + 8);
      $('#loading_text').html(`<span style='color:red'>Error: [${str}] returned. Please tell NixXSkate he's dumb and ${str2}</span>`);
      break;
    default:
      if (!loaded_page) str2 = "re-applying the search/filters or refreshing";
      else str2 = "re-scrolling to the bottom";
      $('#loading_text').html(`<span style='color:red'>Error: [${str}] returned. You can try ${str2} to see if the issue resolves.</span>`);
  }
}

function calcPage() {
  return (Math.floor($(window).scrollTop() / 1350));
}
function calcPageSize(x) {
  return x*27; //warning: 27 is current row height, subject to change $("#list").children()[0].clientHeight
}

function refreshAll() {
  refreshHeaders();
  refreshList();
}

function refreshHeaders() {
  let header_string = "";
  for (let i = 0; i < layout.length; i++) {
    header_string += `<th>${sizeStr(i, headers[layout[i]].size)}<a>${headers[layout[i]].string}</a></div></th>`;
  }
  $("#headers").html(header_string);
}

function addPage(page = 0, refresh = false) {
  if (page == 0) pages.fill("",0,200);
  let body_string = "";
  let bs_class;
  let id = "";
  let start_index = page * page_size;
  let length = players.length;
  if (refresh && page + 1 < loaded_page) {
    length = start_index + page_size;
  }
  for (let i = start_index; i < length; i++) {
    bs_class = (i % 2 ? "normal_row row" : "alt_row row");
    body_string += `<tr id='playr${players[i].rank}' class='${bs_class}'>`;
    for (let j = 0; j < layout.length; j++) {
      id = headers[layout[j]].id ? ` id='${headers[layout[j]].id+players[i].rank}'` : "";
      body_string += `<td${id}>${headers[layout[j]].func(players[i])}</td>` //needs change if adding notes to include alt id
    }
    body_string += "</tr>";
  }
  pages[page] = body_string;
  if (!refresh) loaded_page++;
}

function refreshList(page = -1) {
  if (page < 0) {
    page = calcPage();
    page_current = page;
  }
  let offset = page;
  let last_page = loaded_page - 1;
  let include_pages = [];
  if (page >= 1) {
    include_pages.push(pages[page - 1]);
    offset = page - 1;
  }
  include_pages.push(pages[page]);
  if (page < last_page) include_pages.push(pages[page + 1]);
  let margin_bottom = "";
  let margin_top = "";
  if (offset > 0) {
    margin_top = `<tr class='special_row'><td style='padding-top:${offset * 1350}px'></td></tr>`; //row_height * page_size = 1350
  }
  if (page + 1 < last_page) {
    let bottom_offset = ((last_page - (page + 1)) * 1350) - calcPageSize(50 - page_last); //row_height * page_size = 1350
    margin_bottom = `<tr class='special_row'><td style='padding-top:${bottom_offset}px'></td></tr>`;
  }
  $("#list").html(margin_top + include_pages.join("") + margin_bottom);
  //$("#table_container").css('margin-top', 147+(offset*1350));
  if (page_limit) $("body").css('height', $('#list').height());
  else $("body").css('height', ($('#list').height()+46)+'px'); //46px is the space for the Loading text
}

//currently, $(window).scrollTop for 1 page ranges from 0-1350px, each row is 27px found by $("#list").children()[0].clientHeight
//should be in a global variable once a propet initializer is created

//gonna need this later
//$('body').scrollTop(0);
/*$('body,html').animate({
    'scrollTop': 0,
  }, 750);*/