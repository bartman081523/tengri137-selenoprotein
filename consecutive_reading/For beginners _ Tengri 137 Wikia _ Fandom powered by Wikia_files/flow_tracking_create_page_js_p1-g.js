var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");

define('ext.wikia.flowTracking.createPageTracking',['wikia.flowTracking','wikia.querystring','mw','wikia.document','wikia.window'],function(flowTrack,QueryString,mw,document,window){'use strict';var namespaceId=mw.config.get('wgNamespaceNumber'),articleId=mw.config.get('wgArticleId'),title=mw.config.get('wgTitle');function trackOnEditPageLoad(editor){var qs=new QueryString(window.location),flowParam=qs.getVal('flow',false),tracked=qs.getVal('tracked',false);if(tracked||!isNewArticle()||!isMainNamespace()){return;}
if(flowParam||document.referrer){flowTrack.trackFlowStep(flowParam,{editor:editor});}else{flowTrack.beginFlow(window.wgFlowTrackingFlows.CREATE_PAGE_DIRECT_URL,{editor:editor});qs.setVal('flow',window.wgFlowTrackingFlows.CREATE_PAGE_DIRECT_URL);}
setTrackedQueryParam(qs);}
function trackOnSpecialCreatePageLoad(editor,title){var qs=new QueryString(window.location),flowParam=qs.getVal('flow',false),tracked=qs.getVal('tracked',false);if(tracked||!isAllowedSpecialPage()||!isTitleInMainNamespace(title)){return;}
if(flowParam){flowTrack.trackFlowStep(flowParam,{editor:editor});}else{flowTrack.beginFlow(window.wgFlowTrackingFlows.CREATE_PAGE_SPECIAL_CREATE_PAGE,{editor:editor});qs.setVal('flow',window.wgFlowTrackingFlows.CREATE_PAGE_SPECIAL_CREATE_PAGE);}
setTrackedQueryParam(qs);}
function setTrackedQueryParam(qs){qs.setVal('tracked','true');window.history.replaceState({},'',qs.toString());}
function isNewArticle(){return articleId===0;}
function isAllowedSpecialPage(){return namespaceId===-1&&title==='CreatePage';}
function isMainNamespace(){return namespaceId===0;}
function isTitleInMainNamespace(title){var namespace;title=title||'';if(title.indexOf(':')){namespace=title.split(':')[0].toLowerCase();if(window.wgNamespaceIds[namespace]){return false;}}
return true;}
return{trackOnEditPageLoad:trackOnEditPageLoad,trackOnSpecialCreatePageLoad:trackOnSpecialCreatePageLoad}});;require(['wikia.flowTracking','ext.wikia.flowTracking.createPageTracking','wikia.querystring','mw','jquery','wikia.window'],function(flowTracking,flowTrackingCreatePage,QueryString,mw,$,window){var redLinkFlow=mw.config.get('wgNamespaceNumber')===-1?window.wgFlowTrackingFlows.CREATE_PAGE_SPECIAL_REDLINK:window.wgFlowTrackingFlows.CREATE_PAGE_ARTICLE_REDLINK,createButtonFlow=window.wgFlowTrackingFlows.CREATE_PAGE_CREATE_BUTTON,createboxFlow=window.wgFlowTrackingFlows.CREATE_PAGE_CREATE_BOX,inputBoxFlow=window.wgFlowTrackingFlows.CREATE_PAGE_INPUT_BOX;function init(){var $wikiaArticle=$('#WikiaArticle');$wikiaArticle.find('a.new').each(function(index,redlink){var qs=QueryString(redlink.href);qs.setVal('flow',redLinkFlow);redlink.href=qs.toString();});$wikiaArticle.on('mousedown','a.new',function(e){if(e.which===3){return;}
flowTracking.beginFlow(redLinkFlow,{});});$('form.createboxForm .createboxButton').click(function(){flowTracking.beginFlow(createboxFlow,{});});$('form.createbox').submit(function(){var flowInput=document.createElement('input');flowInput.setAttribute('type','hidden');flowInput.setAttribute('name','flow');flowInput.setAttribute('value',inputBoxFlow);this.appendChild(flowInput);flowTracking.beginFlow(inputBoxFlow,{});});$('#ca-edit').on('mousedown',function(){if(isNewArticle()&&isMainNamespace()){flowTracking.beginFlow(createButtonFlow,{});}});$('#ca-ve-edit').click(function(){if(isNewArticle()&&isMainNamespace()){var qs=new QueryString();flowTracking.beginFlow(createButtonFlow,{});qs.removeVal('tracked');window.history.replaceState({},'',qs.toString());}});}
function initVEHooks(){mw.hook('ve.activationComplete').add(function(){flowTrackingCreatePage.trackOnEditPageLoad('visualeditor');});mw.hook('ve.deactivationComplete').add(function(){var qs=new QueryString(),flow=qs.getVal('flow');if(flow){qs.removeVal('flow');qs.removeVal('tracked');window.history.replaceState({},'',qs.toString())}});mw.hook('ve.afterVEInit').add(function(veEditUri){if(!mw.config.get('wgArticleId')){veEditUri.extend({flow:createButtonFlow});}});}
function isNewArticle(){return mw.config.get('wgArticleId')===0;}
function isMainNamespace(){return mw.config.get('wgNamespaceNumber')===0;}
$(function(){init();initVEHooks();});});;define('wikia.flowTracking',['wikia.log','wikia.tracker','wikia.window','mw','jquery'],function(log,tracker,w,mw,$){'use strict';var flows={CREATE_PAGE_DIRECT_URL:'create-page-direct-url'},track=tracker.buildTrackingFunction({category:'flow-tracking',trackingMethod:'analytics'}),userAgent=w.navigator.userAgent,logGroup='wikia.flowTracking';function beginFlow(flow,extraParams){track(prepareParams(tracker.ACTIONS.FLOW_START,flow,extraParams));}
function trackFlowStep(flow,extraParams){track(prepareParams(tracker.ACTIONS.FLOW_MID_STEP,flow,extraParams));}
function prepareParams(action,flow,extraParams){var params={action:action,flowname:flow,label:flow};extraParams=extraParams||{};params=$.extend(params,extraParams,{useragent:userAgent});log(['prepareParams',params],'debug',logGroup);return params;}
return{beginFlow:beginFlow,trackFlowStep:trackFlowStep,flows:flows};});;
}

/*
     FILE ARCHIVED ON 23:52:52 Jan 08, 2017 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:57:39 Jul 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 11.9
  load_resource: 102.714 (2)
  PetaboxLoader3.datanode: 28.39 (2)
*/