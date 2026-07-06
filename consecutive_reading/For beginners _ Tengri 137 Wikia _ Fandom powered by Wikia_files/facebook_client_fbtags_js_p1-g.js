var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");

mw.hook('wikipage.content').add(function($content){'use strict';if(facebookTagsOnPage()){$.loadFacebookSDK().done(renderFacebookTags);}
function facebookTagsOnPage(){var numOfFacebookTags=$content.find('[data-type="xfbml-tag"], [class^="fb-"]').length;return numOfFacebookTags>0;}
function renderFacebookTags(){FB.XFBML.parse($content[0]);}});;
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
  capture_cache.get: 0.479
  load_resource: 477.921 (2)
  PetaboxLoader3.resolve: 413.234 (2)
  PetaboxLoader3.datanode: 42.137 (2)
*/