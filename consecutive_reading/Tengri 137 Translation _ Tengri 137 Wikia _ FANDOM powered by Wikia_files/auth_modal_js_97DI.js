var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");
(function($,window){'use strict';var authPopUpWindow,closeTrackTimeoutId,popUpWindowHeight=670,popUpWindowMaxWidth=768,popUpName='WikiaAuthWindow',track=getTrackingFunction();function initPostMessageListener(onAuthSuccess){$(window).on('message.authPopUpWindow',function(event){var e=event.originalEvent;if(!e.data){return;}if(e.data.isUserAuthorized){close();if(typeof onAuthSuccess==='function'){onAuthSuccess();}}if(e.data.beforeunload&&!closeTrackTimeoutId){closeTrackTimeoutId=setTimeout(function(){var trackParams;if(authPopUpWindow&&!authPopUpWindow.closed){return;}closeTrackTimeoutId=null;trackParams={action:Wikia.Tracker.ACTIONS.CLOSE,label:'username-login-modal'};if(e.data.forceLogin){trackParams.category='force-login-modal';}track(trackParams);},1000);}});}function close(event){if(event){event.preventDefault();}if(authPopUpWindow){authPopUpWindow.close();}$(window).off('.authPopUpWindow');}function buildPopUpUrl(url,additionalParams){var defaultQueryParams={modal:1,forceLogin:0};
return url+(url.indexOf('?')===-1?'?':'&')+$.param($.extend({},defaultQueryParams,additionalParams));}function getPopUpWindowSpecs(){var pageWidth=window.innerWidth,popUpWindowWidth=pageWidth<popUpWindowMaxWidth?pageWidth:popUpWindowMaxWidth,popUpWindowLeft=window.screenX+(pageWidth/2)-(popUpWindowWidth/2),popUpWindowTop=window.screenY+(window.innerHeight/2)-(popUpWindowHeight/2);return'width='+popUpWindowWidth+',height='+popUpWindowHeight+',top='+popUpWindowTop+',left='+popUpWindowLeft;}function getTrackingFunction(){if(track){return track;}track=Wikia.Tracker.buildTrackingFunction({category:'user-login-desktop-modal',trackingMethod:'analytics'});return track;}function loadPopUpPage(url,forceLogin){var src=buildPopUpUrl(url,{'forceLogin':(forceLogin?1:0)});authPopUpWindow=window.open(src,popUpName,getPopUpWindowSpecs());if(!authPopUpWindow||authPopUpWindow.closed){window.location=url;}}window.wikiaAuthModal={load:function(params){var trackParams={action:Wikia.Tracker.ACTIONS.OPEN,
label:'from-'+params.origin};if(typeof params.onAuthSuccess!=='function'){params.onAuthSuccess=function(){window.location.reload();};}if(!params.origin){params.origin='no-origin-provided';}if(window.wgEnableNewAuthModal){if(params.forceLogin){trackParams.category='force-login-modal';trackParams.label='register-page-from-'+params.origin;}if(!params.url){params.url='/register?redirect='+encodeURIComponent(window.location.href);}initPostMessageListener(params.onAuthSuccess);track(trackParams);loadPopUpPage(params.url,params.forceLogin);}else{window.UserLoginModal.show({origin:params.origin,callback:params.onAuthSuccess});}},close:close};})($,window);;
}

/*
     FILE ARCHIVED ON 17:25:46 Oct 01, 2017 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:51:51 Jul 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 0.484
  load_resource: 2068.986 (2)
  PetaboxLoader3.resolve: 2052.214 (2)
  PetaboxLoader3.datanode: 14.192 (2)
*/