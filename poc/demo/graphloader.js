/* ----------------------------- 
  GRAPH DATA STORE 
    
    Global that stores nodes and links returned from a cypher query
    It is populated by cypherResponseCallback() 
*/

var graphDataStore = {
  linkStore:'',
  nodeArray:'',
  check: function() {
    var badNodeArray = !this.nodeArray || this.nodeArray.length < 1;
    var badLinkStore = !this.linkStore || this.linkStore.length < 1;
    return !badNodeArray && !badLinkStore;
  },//fn
  getNodeArray: function() {return JSON.parse( JSON.stringify( this.nodeArray));}//fn
};



/******************************* 
    LOAD D3 GRAPH CONTROL 

      These functions assume that a successful Cypher query has returned from the server, and that the result are 
      stored in the graphDataStore global.      
*/


function compressAllPaths() { 
  loadGraphWithLinks( graphDataStore.linkStore.compressAll());}//fn

function compressSomePaths( compressThese ){  
  loadGraphWithLinks( graphDataStore.linkStore.compressSome(compressThese));}//fn

function expandSomePaths( expandThese) {
  loadGraphWithLinks( graphDataStore.linkStore.expandSome(expandThese));  }//fn

function expandAllPaths() {
  loadGraphWithLinks( graphDataStore.linkStore.expandAll()); }//fn
  
function loadGraphWithLinks( links ){  
  loadGraphData(  {"nodes": graphDataStore.getNodeArray(), "links": links}); }//fn


/************
  TEST
  
*/
function log( message, data) {
  console.log( message + JSON.stringify(data) );
}


function testCompressAll(){
  log( "compress all ", graphDataStore.linkStore.compressAll());
  compressAllPaths();
}//fn


function testCompressSome() {
    var compressThese = [ {start: "1947" , end: "1958"}, {start: "1947", end: "1980"}];
    log( "compress some", graphDataStore.linkStore.compressSome( compressThese));
    compressSomePaths( compressThese );
}//fn

function testExpandAll() {
    log( "expand all", graphDataStore.linkStore.expandAll());
    expandAllPaths();              
}//fn


function testExpandSome() {
    var expandThese = [ {start: "1947" , end: "1958"}, {start: "1947", end: "1980"}];
    log( "expand some", graphDataStore.linkStore.expandSome( expandThese));
    expandSomePaths( expandThese );
}//fn


