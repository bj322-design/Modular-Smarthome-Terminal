// Main function in order call Spotify and update widget UI
async function updateSpotify() {
    const widget = document.getElementById('widget-Spotify');
    // exit if not found
    if (!widget) return;

    try {
        // Request song that is currently playing 
        const response = await fetch('/api/spotify');
        // Response to JSON 
        const data = await response.json();
        // Spotify UI rendoring 
        widget.innerHTML = `
            <div class="spotify-content">
                <img src="${data.albumArt}" alt="Album Art" class="spotify-album-art">
                <div class="spotify-info">
                    <div class="spotify-track">${data.track}</div>
                    <div class="spotify-artist">${data.artist}</div>
                    <div class="spotify-controls">
                        <button id="spotify-prev">⏮</button>
                        <button id="spotify-playpause">${data.isPlaying ? '⏸' : '▶'}</button>
                        <button id="spotify-next">⏭</button>
                    </div>
                </div>
            </div>
        `;
        // Previous song button
        document.getElementById('spotify-prev')?.addEventListener('click', async () => {
            await fetch('/api/spotify/previous', { method: 'POST' });
            updateSpotify();
        });
        // Play and Pause feature
        document.getElementById('spotify-playpause')?.addEventListener('click', async () => {
            await fetch('/api/spotify/playpause', { method: 'POST' });
            updateSpotify();
        });
        // Next song feature
        document.getElementById('spotify-next')?.addEventListener('click', async () => {
            await fetch('/api/spotify/next', { method: 'POST' });
            updateSpotify();
        });

    } catch (error) {
        console.error('Spotify widget error:', error);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    updateSpotify();
    // Refreshes spotify every 5 seconds 
    setInterval(updateSpotify, 5000);
});