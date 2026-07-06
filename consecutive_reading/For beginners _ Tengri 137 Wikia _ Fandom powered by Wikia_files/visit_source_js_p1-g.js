var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");

var VisitSource=(function(){function VisitSource(cookieName,cookieDomain,isSession){if(isSession===void 0){isSession=true;}
this.cookieExpireDate=new Date(0x7fffffff*1e3);this.cookieName=cookieName;this.cookieDomain=cookieDomain;this.isSession=isSession;}
VisitSource.prototype.checkAndStore=function(){if(this.getCookieValue(this.cookieName,this.getCookie())===null){this.store();}};VisitSource.prototype.store=function(){var referrer=this.getReferrer(),cookieString;cookieString=this.cookieName+'='+encodeURIComponent(referrer);cookieString+=!this.isSession?'; expires='+this.cookieExpireDate.toUTCString():'';cookieString+='; path=/; domain='+this.cookieDomain;this.setCookie(cookieString);};VisitSource.prototype.get=function(){return this.getCookieValue(this.cookieName,this.getCookie());};VisitSource.prototype.getCookieValue=function(name,cookieString){var parts=('; '+cookieString).split('; '+name+'=');if(parts.length===2){return parts.pop().split(';').shift();}
return null;};VisitSource.prototype.getReferrer=function(){return document.referrer;};VisitSource.prototype.setCookie=function(cookieString){document.cookie=cookieString;};VisitSource.prototype.getCookie=function(){return document.cookie;};return VisitSource;})();;$(function(){'use strict';var sessionVisitSource=new VisitSource('WikiaSessionSource',window.wgCookieDomain),lifetimeVisitSource=new VisitSource('WikiaLifetimeSource',window.wgCookieDomain,false);sessionVisitSource.checkAndStore();lifetimeVisitSource.checkAndStore();});;
}

/*
     FILE ARCHIVED ON 23:52:52 Jan 08, 2017 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:57:38 Jul 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 0.456
  load_resource: 88.343 (2)
  PetaboxLoader3.resolve: 41.363
  PetaboxLoader3.datanode: 17.084 (2)
*/