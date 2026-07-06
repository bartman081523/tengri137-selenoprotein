var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");
require(['jquery','wikia.tracker'],function($,tracker){'use strict';var track=tracker.buildTrackingFunction({category:'community-header',trackingMethod:'analytics',action:tracker.ACTIONS.CLICK});$(function(){$('.wds-community-header').on('click','[data-tracking]',function(){track({label:this.dataset.tracking});});});});;require(['wikia.window','jquery'],function(window,$){'use strict';function firstMenuValidator(){var $localNavPreview=$('.local-navigation-preview'),$tabs=$localNavPreview.find('.wds-tabs__tab'),tabsWidth=0;$tabs.each(function(){tabsWidth+=$(this).outerWidth(true);});return tabsWidth<=$localNavPreview.width();}function initPreview(){if(window.wgIsWikiNavMessage){var $saveButton=$('#wpSave');$saveButton.hide().attr('disabled',true);$.getMessages('Oasis-navigation-v2').done(function(){$(window).bind('EditPageAfterRenderPreview',function(ev,previewNode){previewNode.children().removeClass('WikiaArticle');var firstMenuValid=firstMenuValidator(),menuParseError=!!previewNode.
find('nav > ul').attr('data-parse-errors'),errorMessages=[];if(menuParseError){errorMessages.push($.msg('oasis-navigation-v2-magic-word-validation'));}if(!firstMenuValid){errorMessages.push($.msg('oasis-navigation-v2-level1-validation'));}if(errorMessages.length>0){$('#publish').remove();new window.BannerNotification(errorMessages.join('</br>'),'error',$('.modalContent .ArticlePreview')).show();}else{$saveButton.attr('disabled',false);}previewNode.find('nav > ul a').click(function(){if($(this).attr('href')==='#'){return false;}});previewNode.find('.msg > a').click(function(){window.location=this.href;});});});$(window).bind('EditPagePreviewClosed',function(){$saveButton.attr('disabled',true);});$('#wpPreview').parent().removeClass('secondary');$('#EditPageMain').addClass('editpage-wikianavmode');}}$(function(){initPreview();});});;
}

/*
     FILE ARCHIVED ON 17:25:46 Oct 01, 2017 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:51:49 Jul 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 1.453
  load_resource: 246.361 (2)
  PetaboxLoader3.resolve: 210.24
  PetaboxLoader3.datanode: 32.848 (2)
*/