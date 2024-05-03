function getListbox() {
    return document.querySelector('tp-yt-paper-listbox')
}
function addDownloadOption() {
    // number 1
    const menu1 = document.createElement('ytd-menu-service-item-renderer')
    menu1.className=`style-scope ytd-menu-popup-renderer`
    menu1.setAttribute('use-icons',"")
    menu1.role='menuitem'
    menu1.tabIndex=-1
    menu1.innerHTML=`<!--css-build:shady-->
    <!--css-build:shady-->
    <tp-yt-paper-item class="style-scope ytd-menu-service-item-renderer" style-target="host" role="option" tabindex="0" aria-disabled="false"><!--css-build:shady-->
    <yt-icon class="style-scope ytd-menu-service-item-renderer"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M290.001-290.001h379.998v-59.998H290.001v59.998ZM480-413.847 626.153-560 584-602.153l-74.001 72.77v-180.616h-59.998v180.616L376-602.153 333.847-560 480-413.847Zm.067 313.846q-78.836 0-148.204-29.92-69.369-29.92-120.682-81.21-51.314-51.291-81.247-120.629-29.933-69.337-29.933-148.173t29.92-148.204q29.92-69.369 81.21-120.682 51.291-51.314 120.629-81.247 69.337-29.933 148.173-29.933t148.204 29.92q69.369 29.92 120.682 81.21 51.314 51.291 81.247 120.629 29.933 69.337 29.933 148.173t-29.92 148.204q-29.92 69.369-81.21 120.682-51.291 51.314-120.629 81.247-69.337 29.933-148.173 29.933ZM480-160q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"></path></svg><!--css-build:shady--><!--css-build:shady--></yt-icon>
    <yt-formatted-string class="style-scope ytd-menu-service-item-renderer"><!--css-build:shady--><!--css-build:shady--><yt-attributed-string class="style-scope yt-formatted-string">DOWNLOAD</yt-attributed-string></yt-formatted-string>
    <ytd-badge-supported-renderer class="style-scope ytd-menu-service-item-renderer" disable-upgrade="" hidden="">
    </ytd-badge-supported-renderer>

    </tp-yt-paper-item>`
//     getListbox().innerHTML+=`
// <ytd-menu-service-item-renderer class="style-scope ytd-menu-popup-renderer" use-icons="" system-icons="" role="menuitem" tabindex="-1" aria-selected="true">
//     <!--css-build:shady-->
//     <!--css-build:shady-->
//     <tp-yt-paper-item class="style-scope ytd-menu-service-item-renderer" style-target="host" role="option" tabindex="0" aria-disabled="false"><!--css-build:shady-->
//     <yt-icon class="style-scope ytd-menu-service-item-renderer"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M290.001-290.001h379.998v-59.998H290.001v59.998ZM480-413.847 626.153-560 584-602.153l-74.001 72.77v-180.616h-59.998v180.616L376-602.153 333.847-560 480-413.847Zm.067 313.846q-78.836 0-148.204-29.92-69.369-29.92-120.682-81.21-51.314-51.291-81.247-120.629-29.933-69.337-29.933-148.173t29.92-148.204q29.92-69.369 81.21-120.682 51.291-51.314 120.629-81.247 69.337-29.933 148.173-29.933t148.204 29.92q69.369 29.92 120.682 81.21 51.314 51.291 81.247 120.629 29.933 69.337 29.933 148.173t-29.92 148.204q-29.92 69.369-81.21 120.682-51.291 51.314-120.629 81.247-69.337 29.933-148.173 29.933ZM480-160q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"></path></svg><!--css-build:shady--><!--css-build:shady--></yt-icon>
//     <yt-formatted-string class="style-scope ytd-menu-service-item-renderer"><!--css-build:shady--><!--css-build:shady--><yt-attributed-string class="style-scope yt-formatted-string">DOWNLOAD</yt-attributed-string></yt-formatted-string>
//     <ytd-badge-supported-renderer class="style-scope ytd-menu-service-item-renderer" disable-upgrade="" hidden="">
//     </ytd-badge-supported-renderer>

//     </tp-yt-paper-item>
// </ytd-menu-service-item-renderer>`
getListbox().append(menu1)
}
const waitTillDownloadMenuInterval = setInterval(()=>{
    if (getListbox()) {
        addDownloadOption()
        clearInterval(waitTillDownloadMenuInterval)
    }
},5)