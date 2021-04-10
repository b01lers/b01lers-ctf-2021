var globals = {
  canvas: undefined,
  gl: undefined,
  programInfo: undefined,
  buffers: undefined,
  texture: undefined,
  totalTime: 0.0,
  maxTime: 3000.0,
};

init();

function init() {
  const canvas = document.querySelector("#glcanvas");
  const gl = canvas.getContext("webgl", { preserveDrawingBuffer: true });

  if (!gl) {
    alert(
      "Unable to initialize WebGL. Your browser or machine may not support it."
    );
    return;
  }

  // Vertex shader program

  const vsSource = `
    attribute highp vec2 aVertexPosition;

    varying vec2 vPos;

    void main() {
      gl_Position = vec4(aVertexPosition, 0.0, 1.0);
    }
  `;

  // Fragment shader program

  const fsSource = `
    precision highp float;

    varying vec2 vPos;

    uniform sampler2D uSampler;
    uniform vec2 uResolution;
    uniform float uTime;

    uniform float uRadius;
    uniform float uSwirlFactor;

    void main(void) {
      vec2 uv = gl_FragCoord.xy / uResolution.xy;

      float dist = distance(uv, vec2(0.5));
      mat2 rotmat;
      if (dist < uRadius) {
          float percent = (uRadius - dist) / uRadius;
          float angle = percent * percent * uSwirlFactor * uTime;
          float sina = sin(angle);
          float cosa = cos(angle);
          rotmat = mat2(cosa, sina, -sina, cosa);
      } else {
          rotmat = mat2(1, 0, 0, 1);
      }

      vec2 texCoord = rotmat * (uv - vec2(0.5)) + vec2(0.5);
      vec4 diffuse = texture2D(uSampler, texCoord);
      gl_FragColor = diffuse;
    }
  `;

  const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

  // Collect all the info needed to use the shader program.
  // Look up which attributes and uniform locations from our shader program.
  const programInfo = {
    program: shaderProgram,
    attribLocations: {
      vertexPosition: gl.getAttribLocation(shaderProgram, "aVertexPosition"),
    },
    uniformLocations: {
      uSampler: gl.getUniformLocation(shaderProgram, "uSampler"),
      uResolution: gl.getUniformLocation(shaderProgram, "uResolution"),
      uTime: gl.getUniformLocation(shaderProgram, "uTime"),
      uRadius: gl.getUniformLocation(shaderProgram, "uRadius"),
      uSwirlFactor: gl.getUniformLocation(shaderProgram, "uSwirlFactor"),
    },
  };

  // Here's where we call the routine that builds all the
  // objects we'll be drawing.
  const buffers = initBuffers(gl);

  initImageInput(gl);

  globals.canvas = canvas;
  globals.gl = gl;
  globals.shaderProgram = shaderProgram;
  globals.programInfo = programInfo;
  globals.buffers = buffers;
}

function initImageInput(gl) {
  // Add listener for image input

  var input = document.querySelector("#img-input");

  input.addEventListener("change", () => {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = (e) => {
        globals.canvas.removeAttribute("hidden");
        globals.texture = loadTexture(gl, e.target.result, startDrawing);
      };

      reader.readAsDataURL(input.files[0]);
    }
  });
}

function startDrawing() {
  // Render until `globals.maxTime` reached

  var startTime = undefined;
  globals.totalTime = 0.0;

  function render(now) {
    if (startTime === undefined) startTime = now;
    globals.totalTime = now - startTime;

    drawScene(
      globals.gl,
      globals.programInfo,
      globals.buffers,
      globals.texture
    );

    if (globals.totalTime < globals.maxTime) {
      requestAnimationFrame(render);
    }
  }

  requestAnimationFrame(render);
}

function initBuffers(gl) {
  // Create a buffer for a square.
  const positionBuffer = gl.createBuffer();

  // Select the positionBuffer as the one to apply buffer
  // operations to from here out.
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  // Now create an array of positions for the square.
  const positions = makeRectangle(gl, -1.0, -1.0, 2.0, 2.0);

  // Now pass the list of positions into WebGL to build the
  // shape. We do this by creating a Float32Array from the
  // JavaScript array, then use it to fill the current buffer.
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

  return { position: positionBuffer };
}

function loadTexture(gl, url, onload) {
  // Initialize a texture and load an image.
  // When has the image finished loading, call the `onload` callback.

  const texture = gl.createTexture();
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  gl.bindTexture(gl.TEXTURE_2D, texture);

  const image = new Image();
  image.onload = () => {
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(
      gl.TEXTURE_2D,
      0, // level
      gl.RGBA, // internalFormat
      gl.RGBA, // srcFormat
      gl.UNSIGNED_BYTE, // srcType
      image
    );

    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);

    if (onload) onload();
  };
  image.src = url;

  return texture;
}

function drawScene(gl, programInfo, buffers, texture) {
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);

  // Tell WebGL how to pull out the positions from the position
  // buffer into the vertexPosition attribute
  gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
  gl.vertexAttribPointer(
    programInfo.attribLocations.vertexPosition,
    2, // numComponents
    gl.FLOAT, // type
    false, // normalize
    0, // stride
    0 // offset
  );
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);

  // Tell WebGL to use our program when drawing
  gl.useProgram(programInfo.program);

  // Set the shader uniforms

  // Tell WebGL we want to affect texture unit 0.
  // Bind the texture to texture unit 0.
  // Tell the shader we bound the texture to texture unit 0.
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.uniform1i(programInfo.uniformLocations.uSampler, 0);

  // Resolution
  gl.uniform2f(
    programInfo.uniformLocations.uResolution,
    gl.canvas.clientWidth,
    gl.canvas.clientHeight
  );

  // Time
  gl.uniform1f(
    programInfo.uniformLocations.uTime,
    easeInOutCubic(globals.totalTime / globals.maxTime)
  );

  // Swirl parameters
  gl.uniform1f(programInfo.uniformLocations.uRadius, 0.6);
  gl.uniform1f(programInfo.uniformLocations.uSwirlFactor, 12.0);

  {
    const offset = 0;
    const vertexCount = 6;
    gl.drawArrays(gl.TRIANGLES, 0, vertexCount);
  }
}

function initShaderProgram(gl, vsSource, fsSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

  // Create the shader program
  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // If creating the shader program failed, alert
  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert(
      "Unable to initialize the shader program: " +
        gl.getProgramInfoLog(shaderProgram)
    );
    return null;
  }

  return shaderProgram;
}

function loadShader(gl, type, source) {
  // Creates a shader of the given type, uploads the source, and compiles it.

  const shader = gl.createShader(type);

  // Send the source to the shader object
  gl.shaderSource(shader, source);

  // Compile the shader program
  gl.compileShader(shader);

  // See if it compiled successfully
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert(
      "An error occurred compiling the shaders: " + gl.getShaderInfoLog(shader)
    );
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

function easeInOutCubic(x) {
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
}

function makeRectangle(gl, x, y, width, height) {
  var x1 = x;
  var x2 = x + width;
  var y1 = y;
  var y2 = y + height;
  return [x1, y1, x2, y1, x1, y2, x1, y2, x2, y1, x2, y2];
}
