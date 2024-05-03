function createSettings() {
    if (getSettings()) return
    let json={
        video: {
            volume: 1,
            cc: false,
            cc_size:12.5,
            speed: 1,
            theater: false,
            muted:false
        },
        audio: {
            volume: 1,
            autoplay: true,
            lyrics: false
        }
    }
    setSettings(json)
}
function getSettings() {
    return JSON.parse(localStorage.getItem('settings'))
}
function setSettings(json) {
    localStorage['settings'] = JSON.stringify(json)
}
function updateSettings(path, value) {
    // Split the path into individual keys
    const keys = path.replaceAll('/','.');
    const settings=getSettings()
    setSettings(eval('settings.'+keys+'='+JSON.stringify(value)+'\n settings'))
  }
createSettings()