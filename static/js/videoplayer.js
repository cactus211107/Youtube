const id = new URLSearchParams(window.location.search).get('v')
const playPauseBtn = document.querySelector(".play-pause-btn")
const pausePlayIcon = document.querySelector('#pausePlayIcon')
const theaterBtn = document.querySelector(".theater-btn")
const fullScreenBtn = document.querySelector(".full-screen-btn")
const miniPlayerBtn = document.querySelector(".mini-player-btn")
const muteBtn = document.querySelector(".mute-btn")
const captionsBtn = document.querySelector(".captions-btn")
const speedBtn = document.querySelector(".speed-btn")
const currentTimeElem = document.querySelector(".current-time")
const totalTimeElem = document.querySelector(".total-time")
const previewImg = document.querySelector(".preview-img")
const thumbnailImg = document.querySelector(".thumbnail-img")
const volumeSlider = document.querySelector(".volume-slider")
const videoContainer = document.querySelector(".video-container")
const timelineContainer = document.querySelector(".timeline-container")
const caption_track = document.querySelector('.caption_track')
const castBtn = document.querySelector('.screen-cast-btn')
const display_caption_elm = document.querySelector('.caption_track>div>div')
const caption_font_size_change = 6.25;
const caption_font_size_min = 12.5;
const caption_font_size_max = 50;
// const captions = getCaptions()
const video = document.querySelector("video")

document.addEventListener("keydown", e => {
  const tagName = document.activeElement.tagName.toLowerCase()
  if (tagName === "input") return

  switch (e.key.toLowerCase()) {
    case " ":
      e.preventDefault()
    case "k":
      togglePlay()
      break
    case "f":
      toggleFullScreenMode()
      break
    case "t":
      toggleTheaterMode()
      break
    case "i":
      toggleMiniPlayerMode()
      break
    case "m":
      toggleMute()
      break
    case "arrowleft":
    case "j":
      skip(-5)
      break
    case "arrowright":
    case "l":
      skip(5)
      break
    case "c":
      toggleCaptions()
      break
    case "=":
    case "+":
      increaseCaptionSize()
      break
    case "-":
      decreaseCaptionSize()
      break
    case "v":
      screenCast()
      break
  }
})
function getCaptionFontSize() {
  return parseFloat(getComputedStyle(display_caption_elm).fontSize.slice(0, -2))
}
function setFontSizeBetweenConstrains(size) {
  size=Math.max(Math.min(size, caption_font_size_max), caption_font_size_min)
  display_caption_elm.style.fontSize = size + 'px'
  updateSettings('video/cc_size',size)
}
function increaseCaptionSize() {
  setFontSizeBetweenConstrains(getCaptionFontSize() + caption_font_size_change)
}
function decreaseCaptionSize() {
  setFontSizeBetweenConstrains(getCaptionFontSize() - caption_font_size_change)
}
// Timeline
timelineContainer.addEventListener("mousemove", handleTimelineUpdate)
timelineContainer.addEventListener("mousedown", toggleScrubbing)
document.addEventListener("mouseup", e => {
  if (isScrubbing) toggleScrubbing(e)
})
document.addEventListener("mousemove", e => {
  if (isScrubbing) handleTimelineUpdate(e)
})

let isScrubbing = false
let wasPaused
function toggleScrubbing(e) {
  const rect = timelineContainer.getBoundingClientRect()
  const percent = Math.min(Math.max(0, e.x - rect.x), rect.width) / rect.width
  isScrubbing = (e.buttons & 1) === 1
  videoContainer.classList.toggle("scrubbing", isScrubbing)
  if (isScrubbing) {
    wasPaused = video.paused
    video.pause()
  } else {
    video.currentTime = percent * video.duration
    if (!wasPaused) video.play()
  }

  handleTimelineUpdate(e)
}

function handleTimelineUpdate(e) {
  const rect = timelineContainer.getBoundingClientRect()
  const percent = Math.min(Math.max(0, e.x - rect.x), rect.width) / rect.width
  const previewImgNumber = Math.max(
    1,
    Math.floor((percent * video.duration) / 5)
  )
  const previewImgSrc = `downloaded/videos/${id}/previews/preview${previewImgNumber}.jpg`
  previewImg.src = previewImgSrc
  timelineContainer.style.setProperty("--preview-position", percent)

  if (isScrubbing) {
    e.preventDefault()
    thumbnailImg.src = previewImgSrc
    timelineContainer.style.setProperty("--progress-position", percent)
  }
}

// Playback Speed
speedBtn.addEventListener("click", changePlaybackSpeed)
const playbackRate_minimum = 0.25;
const playbackRate_maximum = 2;
const playbackRate_change = 0.25;
function changePlaybackSpeed() {
  let newPlaybackRate = video.playbackRate + playbackRate_change
  if (newPlaybackRate > playbackRate_maximum) newPlaybackRate = playbackRate_minimum
  video.playbackRate = newPlaybackRate
  speedBtn.textContent = `${newPlaybackRate}x`
  updateSettings('video/speed',newPlaybackRate)
}
function setPlaybackSpeed(speed) {
  video.playbackRate = speed
  speedBtn.textContent = `${speed}x`
  updateSettings('video/speed',speed)
}

// Captions

captionsBtn.addEventListener("click", toggleCaptions)

function toggleCaptions() {
  const isHidden = getComputedStyle(caption_track).display === 'none'
  // caption_track.style.display = isHidden ? "flex" : 'none'
  videoContainer.classList.toggle("captions", isHidden)
  updateSettings('video/cc',isHidden)
}

// Duration
video.addEventListener("loadeddata", () => {
  totalTimeElem.textContent = formatDuration(video.duration)
})

video.addEventListener("timeupdate", () => {
  currentTimeElem.textContent = formatDuration(video.currentTime)
  const percent = video.currentTime / video.duration
  timelineContainer.style.setProperty("--progress-position", percent)
})

const leadingZeroFormatter = new Intl.NumberFormat(undefined, {
  minimumIntegerDigits: 2,
})
function formatDuration(time) {
  const seconds = Math.floor(time % 60)
  const minutes = Math.floor(time / 60) % 60
  const hours = Math.floor(time / 3600)
  if (hours === 0) {
    return `${minutes}:${leadingZeroFormatter.format(seconds)}`
  } else {
    return `${hours}:${leadingZeroFormatter.format(
      minutes
    )}:${leadingZeroFormatter.format(seconds)}`
  }
}

function skip(duration) {
  video.currentTime += duration
}

// Volume
function setCssVolume() {
  volumeSlider.style.setProperty('--volume', volumeSlider.value * 100 + '%')
  updateSettings('video/volume',volumeSlider.value)
  updateSettings('video/muted',false)
}
muteBtn.addEventListener("click", toggleMute)
volumeSlider.addEventListener("input", e => {
  video.volume = e.target.value
  video.muted = e.target.value === 0
  setCssVolume()
})

function toggleMute() {
  video.muted = !video.muted
  updateSettings('video/muted',video.muted)
}

video.addEventListener("volumechange", () => {
  volumeSlider.value = video.volume
  let volumeLevel
  if (video.muted || video.volume === 0) {
    volumeSlider.value = 0
    volumeLevel = "muted"
  } else if (video.volume >= 0.5) {
    volumeLevel = "high"
  } else {
    volumeLevel = "low"
  }

  videoContainer.dataset.volumeLevel = volumeLevel
  setCssVolume()
  updateSettings('video/volume',video.volume)
})

// View Modes
theaterBtn.addEventListener("click", toggleTheaterMode)
fullScreenBtn.addEventListener("click", toggleFullScreenMode)
miniPlayerBtn.addEventListener("click", toggleMiniPlayerMode)

function toggleTheaterMode() {
  updateSettings('video/theater',!getSettings().video.theater)
  videoContainer.classList.toggle("theater")
}

function toggleFullScreenMode() {
  if (document.fullscreenElement == null) {
    videoContainer.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

function toggleMiniPlayerMode() {
  if (videoContainer.classList.contains("mini-player")) {
    document.exitPictureInPicture()
  } else {
    video.requestPictureInPicture()
  }
}

document.addEventListener("fullscreenchange", () => {
  videoContainer.classList.toggle("full-screen", document.fullscreenElement)
})

video.addEventListener("enterpictureinpicture", () => {
  videoContainer.classList.add("mini-player")
})

video.addEventListener("leavepictureinpicture", () => {
  videoContainer.classList.remove("mini-player")
})

// Play/Pause
playPauseBtn.addEventListener("click", togglePlay)
video.addEventListener("click", togglePlay)


const play_path = 'M 12,26 18.5,22 18.5,14 12,10 z M 18.5,22 25,18 25,18 18.5,14 z';
const pause_path = "M 12,26 16,26 16,10 12,10 z M 21,26 25,26 25,10 21,10 z"
const play_to_pause=[
  "M 12,26 18.401693190707515,22.157290894867973 18.401693190707515,13.842709105132027 12,10 z M 18.598306809292485,22.157290894867973 25,18.314581789735946 25,17.685418210264054 18.598306809292485,13.842709105132027 z",
  "M 12,26 18.202084844125736,22.476664249398823 18.202084844125736,13.523335750601177 12,10 z M 18.797915155874264,22.476664249398823 25,18.953328498797646 25,17.046671501202354 18.797915155874264,13.523335750601177 z",
  "M 12,26 18.06243376241639,22.700105980133774 18.06243376241639,13.299894019866226 12,10 z M 18.93756623758361,22.700105980133774 25,19.400211960267548 25,16.599788039732452 18.93756623758361,13.299894019866226 z",
  "M 12,26 17.934276814117016,22.905157097412776 17.934276814117016,13.094842902587226 12,10 z M 19.065723185882984,22.905157097412776 25,19.810314194825548 25,16.189685805174452 19.065723185882984,13.094842902587226 z",
  "M 12,26 17.821181255062758,23.086109991899587 17.821181255062758,12.913890008100411 12,10 z M 19.178818744937242,23.086109991899587 25,20.172219983799177 25,15.827780016200823 19.178818744937242,12.913890008100411 z",
  "M 12,26 17.711826091565385,23.261078253495384 17.711826091565385,12.738921746504614 12,10 z M 19.288173908434615,23.261078253495384 25,20.522156506990772 25,15.477843493009228 19.288173908434615,12.738921746504614 z",
  "M 12,26 17.591232175483952,23.454028519225673 17.591232175483952,12.545971480774327 12,10 z M 19.408767824516048,23.454028519225673 25,20.908057038451346 25,15.091942961548654 19.408767824516048,12.545971480774327 z",
  "M 12,26 17.440464193030582,23.695257291151066 17.440464193030582,12.304742708848934 12,10 z M 19.559535806969418,23.695257291151066 25,21.39051458230213 25,14.609485417697867 19.559535806969418,12.304742708848934 z",
  "M 12,26 17.254650067591815,23.992559891853098 17.254650067591815,12.007440108146902 12,10 z M 19.745349932408185,23.992559891853098 25,21.985119783706196 25,14.014880216293806 19.745349932408185,12.007440108146902 z",
  "M 12,26 17.0239263125,24.3617179 17.0239263125,11.6382821 12,10 z M 19.9760736875,24.3617179 25,22.7234358 25,13.2765642 19.9760736875,11.6382821 z",
  "M 12,26 16.720424934249657,24.847320105200552 16.720424934249657,11.152679894799448 12,10 z M 20.279575065750343,24.847320105200552 25,23.694640210401104 25,12.305359789598898 20.279575065750343,11.152679894799448 z",
  "M 12,26 16.33643641351743,25.461701738372117 16.33643641351743,10.538298261627885 12,10 z M 20.66356358648257,25.461701738372117 25,24.92340347674423 25,11.07659652325577 20.66356358648257,10.538298261627885 z",
]
const pause_to_play=[
  "M 12,26 16.032460115393295,25.94806381537073 16.032460115393295,10.051936184629271 12,10 z M 20.967539884606705,25.94806381537073 25,25.896127630741457 25,10.103872369258541 20.967539884606705,10.051936184629271 z",
  "M 12,26 16.150780146753476,25.758751765194436 16.150780146753476,10.241248234805564 12,10 z M 20.849219853246524,25.758751765194436 25,25.517503530388872 25,10.482496469611128 20.849219853246524,10.241248234805564 z",
  "M 12,26 16.297915155874264,25.523335750601177 16.297915155874264,10.476664249398823 12,10 z M 20.702084844125736,25.523335750601177 25,25.046671501202354 25,10.953328498797648 20.702084844125736,10.476664249398823 z",
  "M 12,26 16.449474849798946,25.280840240321687 16.449474849798946,10.719159759678314 12,10 z M 20.550525150201054,25.280840240321687 25,24.56168048064337 25,11.438319519356627 20.550525150201054,10.719159759678314 z",
  "M 12,26 16.576427317678643,25.07771629171417 16.576427317678643,10.92228370828583 12,10 z M 20.423572682321357,25.07771629171417 25,24.15543258342834 25,11.84456741657166 20.423572682321357,10.92228370828583 z",
  "M 12,26 16.683424,24.9065216 16.683424,11.0934784 12,10 z M 20.316576,24.9065216 25,23.8130432 25,12.1869568 20.316576,11.0934784 z",
  "M 12,26 16.792264884828317,24.732376184274692 16.792264884828317,11.267623815725306 12,10 z M 20.207735115171683,24.732376184274692 25,23.464752368549387 25,12.535247631450613 20.207735115171683,11.267623815725306 z",
  "M 12,26 16.91270842767279,24.539666515723535 16.91270842767279,11.460333484276465 12,10 z M 20.08729157232721,24.539666515723535 25,23.07933303144707 25,12.920666968552931 20.08729157232721,11.460333484276465 z",
  "M 12,26 17.063474,24.2984416 17.063474,11.7015584 12,10 z M 19.936526,24.2984416 25,22.5968832 25,13.4031168 19.936526,11.7015584 z",
  "M 12,26 17.2478676875,24.0034117 17.2478676875,11.996588299999999 12,10 z M 19.7521323125,24.0034117 25,22.006823400000002 25,13.9931766 19.7521323125,11.996588299999999 z",
  "M 12,26 17.4857440312155,23.622809550055198 17.4857440312155,12.377190449944802 12,10 z M 19.5142559687845,23.622809550055198 25,21.245619100110396 25,14.754380899889604 19.5142559687845,12.377190449944802 z",
  "M 12,26 17.793955838201093,23.12967065887825 17.793955838201093,12.87032934112175 12,10 z M 19.206044161798907,23.12967065887825 25,20.2593413177565 25,15.740658682243499 19.206044161798907,12.87032934112175 z",
  "M 12,26 18.1790364375,22.5135417 18.1790364375,13.486458299999999 12,10 z M 18.8209635625,22.5135417 25,19.027083400000002 25,16.972916599999998 18.8209635625,13.486458299999999 z",
]
function runAnimation(time=200) {
  const state = video.paused
  console.log(state)
  const animation = state ? play_to_pause:pause_to_play
  let frame=0;
  const interval=setInterval(()=>{
    // console.log(frame)
    // console.log(animation[frame])
    pausePlayIcon.setAttribute('d',animation[frame])
    frame++;
    if (frame==animation.length){
      // console.log(state ? 'play_path':'pause_path')
      pausePlayIcon.setAttribute('d',!state ? play_path:pause_path)
      clearInterval(interval)
    }
  },time/animation.length)
}


function togglePlay() {
  runAnimation()
  video.paused ? video.play() : video.pause()
}

video.addEventListener("play", () => {
  videoContainer.classList.remove("paused")
})

video.addEventListener("pause", () => {
  videoContainer.classList.add("paused")
})
castBtn.addEventListener('click',()=>{
  launchApp()
})

async function timed_captions(video, caption_element, captions) {
  // video.addEventListener('timeupdate', displayCaption);
  setInterval(displayCaption,50)
  function displayCaption() {
    if (video.paused) return
    const MAX_LINES = 3;
    let line_counter=0;
    let caption_text = ''
    const currentTime = video.currentTime;
    for (const caption of captions) {
      if (line_counter >= 3) break
      if (currentTime >= caption.start && currentTime <= caption.end) {
        for (const block of caption.blocks) {
          // console.log('start',caption.start,'end',caption.end,'block offset',block.offset,'block start',caption.start + block.offset,'current time', currentTime)
          if (currentTime>=caption.start + block.offset) {
            caption_text += block.text
          }
        }
        caption_text+='\n'
        line_counter++;
        caption_element.textContent = caption_text;
        // break;
      } else {
        caption_element.textContent = ''
      }
    }
  }
}
async function captions() {
  await fetch(`/captions?id=${id}`).then(response => response.json()).then(result => {
    // result = JSON.parse(result)
    timed_captions(video, display_caption_elm, result)
  })
}
var currentTime = 0; // Initialize current time

window['__onGCastApiAvailable'] = function (isAvailable) {
    if (isAvailable) {
        initializeCastApi();
    }
};

function initializeCastApi() {
    var sessionRequest = new chrome.cast.SessionRequest(chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID);
    var apiConfig = new chrome.cast.ApiConfig(sessionRequest, sessionListener, receiverListener);
    chrome.cast.initialize(apiConfig, onInitSuccess, onError);
}

function receiverListener(availability) {
    if (availability === chrome.cast.ReceiverAvailability.AVAILABLE) {
        console.log('Receiver available');
        // Display available devices or trigger casting UI
    } else {
        console.log('No receiver available');
    }
}
function sessionListener(session) {
  console.log('Session listener:', session);
  // Additional session handling logic if needed
}

function launchApp() {
    currentTime = video.currentTime;
    chrome.cast.requestSession(onRequestSessionSuccess, onError);
}

function onRequestSessionSuccess(session) {
    var mediaInfo = new chrome.cast.media.MediaInfo(video.src);
    var request = new chrome.cast.media.LoadRequest(mediaInfo);
    
    // Set the start time of the video
    request.currentTime = currentTime;
    request.

    session.loadMedia(request, onMediaDiscovered, onError);
}

function onInitSuccess() {
    console.log('Cast API initialized');
    // Additional initialization logic if needed
}

function onMediaDiscovered() {
    console.log('Media discovered');
    // Additional logic after media is discovered
}

function onError(error) {
    console.error('Error:', error);
}
setCssVolume()
captions()
// set the settigs
const settings = getSettings().video
setFontSizeBetweenConstrains(settings.cc_size)
video.muted=settings.muted
video.volume=settings.volume
setPlaybackSpeed(settings.speed)
if (settings.cc)toggleCaptions()
if (settings.theater)toggleTheaterMode()