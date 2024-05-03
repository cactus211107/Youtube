let last_start_ms = 0;
function getCaptionText(caption) {
    let formatted = ''
    for (let i = 0; i < caption.segs.length; i++) {
        const segment = caption.segs[i];
        let text = segment.utf8.trim()
        if (i>0) {
            formatted+=' ('+text+')'
            continue
        }
        formatted+=text
    }
    return formatted.trim()
}
async function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}
async function play_captions(captions,play_function) { // play_function are callback function when that event occurs
    for (const caption of captions) {
        const ms_start_time = caption.tStartMs;
        const wait_for = (ms_start_time - last_start_ms) / 1000;
        await sleep(wait_for);
        play_function(getCaptionText(caption));
        last_start_ms = ms_start_time;
      }
}
async function play_in_console(captions) {
  await play_captions(captions,console.log)
}
async function play_in_element(element,captions,hide_delay) {
    let last_updated = new Date().getTime()
    const interval = setInterval(()=>{
        if (new Date().getTime()-last_updated >= hide_delay*1000) {
            element.innerHTML=''
        }
    },50)
    await play_captions(captions,(caption)=>{
        element.innerHTML = caption;
        last_updated = new Date().getTime()
    })
    clearInterval(interval)
}

// async function play_in_video(video,caption_element,captions) {
//     video.addEventListener('timeupdate', displayCaption);
//     function displayCaption() {
//         const currentTime = video.currentTime*1000;
//         for (const caption of captions) {
//             if (currentTime >= caption.tStartMs && currentTime <= caption.tStartMs+caption.dDurationMs) {
//                 caption_element.textContent = getCaptionText(caption);
//                 break;
//             } else {
//                 caption_element.textContent=''
//             }
//         }
//     }
// }
async function play_in_video(video,caption_element,captions) {
    video.addEventListener('timeupdate', displayCaption);
    function displayCaption() {
        const currentTime = video.currentTime;
        for (const caption of captions) {
            if (currentTime >= caption.start && currentTime <= caption.start+caption.duration) {
                caption_element.textContent = caption.text;
                break;
            } else {
                caption_element.textContent=''
            }
        }
    }
}
async function timed_captions(video,caption_element,captions) {
    video.addEventListener('timeupdate', displayCaption);
    function displayCaption() {
        const currentTime = video.currentTime;
        for (const caption of captions) {
            if (currentTime >= caption.start && currentTime <= caption.end) {
                console.log('in caption block time')
                let caption_text=''
                for (const block of caption.block) {
                    if (caption.start+block.offset >= currentTime) {
                        caption_text+=block.text
                    }
                }
                console.log(caption.text)
                caption_element.textContent = caption.text;
                caption_element.setAttribute('data-textContent',caption.text)
                break;


            } else {
                console.log('empty')
                caption_element.textContent=''
                
            }
        }
    }
}