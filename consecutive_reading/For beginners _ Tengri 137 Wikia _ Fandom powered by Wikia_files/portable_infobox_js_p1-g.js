var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");

(function(window,$){'use strict';var ImageCollection={init:function($content){var $imageCollections=$content.find('.pi-image-collection');$imageCollections.each(function(index,collection){var $collection=$imageCollections.eq(index),$tabs=$collection.find('ul.pi-image-collection-tabs li'),$tabContent=$collection.find('.pi-image-collection-tab-content');$tabs.click(function(){var $target=$(this),tabId=$target.attr('data-pi-tab');$tabs.removeClass('current');$tabContent.removeClass('current');$target.addClass('current');$collection.find('#'+tabId).addClass('current');});});}};var CollapsibleGroup={init:function($content){var $collapsibleGroups=$content.find('.pi-collapse');$collapsibleGroups.each(function(index,group){var $group=$collapsibleGroups.eq(index),$header=$group.find('.pi-header');$header.click(function(){$group.toggleClass('pi-collapse-closed');});});}};mw.hook('wikipage.content').add(function($content){ImageCollection.init($content);CollapsibleGroup.init($content);});})(window,jQuery);;
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
  capture_cache.get: 1.137
  load_resource: 454.313 (2)
  PetaboxLoader3.resolve: 350.484
  PetaboxLoader3.datanode: 67.357 (2)
*/