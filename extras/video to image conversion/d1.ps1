# Example of capturing progress and updating a PowerShell progress bar
Start-Process ffmpeg -ArgumentList @(
    '-i', 'PCA.mp4',
    '-vf', 'select=''gt(scene,0.001)'',showinfo',
    '-vsync', 'vfr',
    '-progress', 'pipe:2',
    'frames/out_%03d.png'
) -NoNewWindow -PassThru |
  ForEach-Object {
      # Here you'd parse each line of stderr looking for lines like "progress=continue" or "out_time_ms=123456"
      # Then update Write-Progress accordingly.
  }
