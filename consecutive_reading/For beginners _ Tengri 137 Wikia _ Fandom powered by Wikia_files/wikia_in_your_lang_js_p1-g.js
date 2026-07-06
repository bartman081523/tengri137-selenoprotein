var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");

require(['jquery','mw','wikia.window','wikia.geo','wikia.cache','wikia.tracker','BannerNotification'],function($,mw,w,geo,cache,tracker,BannerNotification){'use strict';var targetLanguage=getTargetLanguage(),contentLanguage=w.wgContentLanguage,cacheVersion='1.02',linkTitle=retrieveLinkTitle();function init(){var interlangExist=false;if(targetLanguage!==false&&shouldShowWikiaInYourLang(targetLanguage,contentLanguage)&&cache.get(getWIYLNotificationShownKey())!==true){if(cache.get(getWIYLRequestSentKey())!==true){interlangExist=getInterlangFromArticleInterlangList();if(!interlangExist){getNativeWikiaInfo();}}else if(typeof cache.get(getWIYLMessageKey())==='string'){displayNotification(cache.get(getWIYLMessageKey()));}}}
function shouldShowWikiaInYourLang(targetLanguage,contentLanguage){var targetLanguageLangCode=targetLanguage.split('-')[0],contentLanguageLangCode=contentLanguage.split('-')[0],targetLanguageFilter=['zh','ko','vi','ru','ja'];if(targetLanguageFilter.indexOf(targetLanguageLangCode)===-1){return false;}
return targetLanguageLangCode!==contentLanguageLangCode;}
function getTargetLanguage(){var browserLanguage=window.navigator.language||window.navigator.userLanguage,geoCountryCode=geo.getCountryCode().toLowerCase(),targetLanguage;if(w.wgUserName!==null){targetLanguage=w.wgUserLanguage;}else if(typeof browserLanguage==='string'){targetLanguage=browserLanguage.split('-')[0];}else if(typeof geoCountryCode==='string'){targetLanguage=geoCountryCode;}else{targetLanguage=false;}
return targetLanguage;}
function getInterlangFromArticleInterlangList(){var i,interlangData;if(Array.isArray(w.wgArticleInterlangList)){for(i=0;i<w.wgArticleInterlangList.length;i++){interlangData=w.wgArticleInterlangList[i].split(':');if(targetLanguage===interlangData[0]){getNativeWikiaInfo(interlangData[1]);return true;}}}
return false;}
function getNativeWikiaInfo(interlangTitle){$.nirvana.sendRequest({controller:'WikiaInYourLangController',method:'getNativeWikiaInfo',format:'json',type:'GET',data:{targetLanguage:targetLanguage,articleTitle:w.wgPageName,interlangTitle:interlangTitle},callback:function(results){if(results.success===true){saveLinkTitle(results.linkAddress);linkTitle=retrieveLinkTitle();displayNotification(results.message);cache.set(getWIYLRequestSentKey(),true,cache.CACHE_STANDARD);cache.set(getWIYLMessageKey(),results.message,cache.CACHE_STANDARD);}}});}
function displayNotification(message){var bannerNotification=new BannerNotification(message,'notify').show(),label=getTrackingLabel('notification-view'),trackingParams={trackingMethod:'analytics',category:'wikia-in-your-lang',action:tracker.ACTIONS.VIEW,label:label};tracker.track(trackingParams);bindEvents(bannerNotification);}
function bindEvents(bannerNotification){bannerNotification.onClose(onNotificationClosed);bannerNotification.$element.on('click','.text',onLinkClick);}
function onNotificationClosed(){var label=getTrackingLabel('notification-close'),trackingParams={trackingMethod:'analytics',category:'wikia-in-your-lang',action:tracker.ACTIONS.CLOSE,label:label,};tracker.track(trackingParams);cache.set(getWIYLMessageKey(),null);cache.set(getWIYLNotificationShownKey(),true,cache.CACHE_LONG);}
function onLinkClick(){var label=getTrackingLabel('notification-link-click'),trackingParams={trackingMethod:'analytics',category:'wikia-in-your-lang',action:tracker.ACTIONS.CLICK_LINK_TEXT,label:label,};tracker.track(trackingParams);}
function getWIYLRequestSentKey(){return'wikiaInYourLangRequestSent'+linkTitle+cacheVersion;}
function getWIYLNotificationShownKey(){return'wikiaInYourLangNotificationShown'+cacheVersion;}
function getWIYLMessageKey(){return targetLanguage+'WikiaInYourLangMessage'+linkTitle+cacheVersion;}
function getWIYLLinkTitlesKey(){return targetLanguage+'WikiaInYourLangLinkTitles'+cacheVersion;}
function saveLinkTitle(linkAddress){var articleTitle=w.wgPageName,linkAddressAry=linkAddress.match(/.+\.com\/wiki\/(.*)/),listOfCachedTitles={},linkTitle='';if(linkAddressAry&&linkAddressAry.length>1){linkTitle=linkAddressAry[1];}else{linkTitle='main';}
listOfCachedTitles=cache.get(getWIYLLinkTitlesKey());if(!listOfCachedTitles){listOfCachedTitles={};}
listOfCachedTitles[articleTitle]=linkTitle;cache.set(getWIYLLinkTitlesKey(),listOfCachedTitles,cache.CACHE_LONG);}
function retrieveLinkTitle(){var articleTitle=w.wgPageName,listOfCachedTitles=cache.get(getWIYLLinkTitlesKey());return(listOfCachedTitles&&listOfCachedTitles[articleTitle])?listOfCachedTitles[articleTitle]:'';}
function getTrackingLabel(postfix){var label=targetLanguage;if(linkTitle.length>0&&linkTitle!='main'){label+='-article';}
label+='-'+postfix;return label;}
if(!w.wikiaPageIsCorporate){$(init);}});;
}

/*
     FILE ARCHIVED ON 23:52:51 Jan 08, 2017 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:57:38 Jul 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 0.552
  load_resource: 252.293 (2)
  PetaboxLoader3.resolve: 185.334 (2)
  PetaboxLoader3.datanode: 49.213 (2)
*/