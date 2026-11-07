// Source-only export configuration. Native mode retains one texel per source pixel.
export function renderGeometry(width, height, mode = 'legacy') {
  if (![width, height].every(n => Number.isInteger(n) && n >= 100 && n <= 4096))
    throw Error('Invalid source canvas');
  if (mode === 'legacy') {
    const scale = Math.min(460 / width, 450 / height);
    return {width:480, height:480, scale, x:(480-width*scale)/2, y:(480-height*scale)/2};
  }
  if (mode !== 'native') throw Error('Unknown export mode');
  // Integer registration; margin accommodates the existing +/-1.6 px portrait motion.
  return {width:2*Math.ceil((width+32)/2), height:2*Math.ceil((height+32)/2), scale:1, x:16, y:16};
}

export function privacyClass(status) {
  if (status === 'SYNTHETIC_CALIBRATION_ONLY') return status;
  if (status === 'PRIVATE_CANONICAL_EXPERIMENTAL') return 'PRIVATE_ARTWORK';
  throw Error('Unknown artwork privacy status');
}

export function validateStreams(streams, geometry) {
  const v = streams.find(s => s.codec_type === 'video');
  const a = streams.find(s => s.codec_type === 'audio');
  if (!v || !a || Number(v.nb_read_frames) !== 120 || v.r_frame_rate !== '24/1' ||
      v.width !== geometry.width || v.height !== geometry.height ||
      Math.abs(Number(v.duration)-5) > 0.05 || !Number.isFinite(Number(v.duration)) ||
      Math.abs(Number(a.duration)-5) > 0.05 || !Number.isFinite(Number(a.duration)))
    throw Error('Invalid 120-frame video/audio export');
  return {video:v, audio:a};
}
