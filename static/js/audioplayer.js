const audio=document.querySelector('audio')
const play_pause_btn=document.querySelector('.play-pause-btn')
const prev_btn=document.querySelector('.previous-song-btn')
const next_btn=document.querySelector('.next-song-btn')
const shuffle_toggle=document.querySelector('.shuffle-btn')
const reshuffle_button=document.querySelector('.reshuffle-btn')
const timeline=document.querySelector("#timeline")
const cover_elm = document.querySelector('.cover > img')
const name_elm = document.querySelector('.song > h1')
const artists_elm = document.querySelector('.song > span')
document.body.click()
var songs=[]
var alternate_playlist,playlist
fetch('/songs').then(response=>response.json()).then(result=>{
    songs=result
    alternate_playlist=songs //used for when toggling shuffle on/off
    playlist = songs
})

document.addEventListener("keydown", e => {
    const tagName = document.activeElement.tagName.toLowerCase()
    console.log(e.key.toLowerCase())
    if (tagName === "input") return

    switch (e.key.toLowerCase()) {
        case " ":
            e.preventDefault()
            playPause()
        case "arrowleft":
        case "j":
            previousSong()
        break
        case "arrowright":
        case "l":
            nextSong()
        break
        case "l":
            toggleLyrics()
        break
        case "=":
        case "+":
            increaseCaptionSize()
        break
        case "-":
            decreaseCaptionSize()
        break
    }
})
function getSongIndex() {
    return playlist.indexOf(playlist.find(x=>x[0]==window.location.pathname.split('/').at(-1)))
}
function loopIndex(index) {
    return (songs.length+index)%songs.length
}
function playSong(index,start=0) {
    index=loopIndex(index)
    let song=playlist[index]
    let id=song[0]
    audio.src='/downloaded/audio/'+id+'/audio.mp3'
    audio.currentTime=start
    audio.play()
    window.history.pushState({},'','/spotify/track/'+id)
    // update info
    cover_elm.src = '/downloaded/audio/'+id+'/cover.jpg'
    name_elm.textContent = song[1]
    let _artists = ''
    for (const _artist of JSON.parse(song[2])) {
        _artists+=_artist.name+', '
    }
    artists_elm.textContent = _artists.slice(0,-2)
    
}
function reshuffleList(list) {
    let reshuffled=[]
    let len=list.length
    for (let i = 0; i < len; i++) {
        reshuffled.push(list.splice(Math.floor(Math.random()*list.length),1)[0])
    }
    return reshuffled
}
function playPause() {
    audio.paused?audio.play():audio.pause()
}
function toggleLyrics() {

}
function nextSong() {
    playSong(getSongIndex()+1)
}
function previousSong() {
    if (audio.currentTime < 3) {
        playSong(getSongIndex()-1)
    } else {
        playSong(getSongIndex())
    }
}
function increaseCaptionSize() {
    
}
function decreaseCaptionSize() {
    
}
var timelineMouseDown = false;
timeline.addEventListener("mousedown", function () {
    timelineMouseDown = true;
});
document.addEventListener("mouseup", function () {
    timelineMouseDown = false;
});
function updateTimeline() {
    timeline.value=audio.currentTime/audio.duration*100
    timeline.style.setProperty('--percent',timeline.value+'%')
}
timeline.addEventListener('input',()=>{
    audio.currentTime=audio.duration*timeline.value/100
    updateTimeline()
})
// document.createElement('input').on
audio.ontimeupdate=()=>{
    if (timelineMouseDown)return
    updateTimeline()
}
audio.onended=nextSong
play_pause_btn.addEventListener('click',playPause)
next_btn.addEventListener('click',nextSong)
prev_btn.addEventListener('click',previousSong)
shuffle_toggle.addEventListener('click',()=>{
    let _=playlist
    playlist=alternate_playlist
    alternate_playlist=_
})
reshuffle_button.addEventListener('click',reshuffleList)