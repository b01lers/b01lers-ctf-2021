#include <stdlib.h>
#include <stdio.h>

const int SAMPLE_RATE = 44100;
const int ONE_FREQ = 2400;
const int ZERO_FREQ = 1200;
const int ZERO_CYCLES_PER_BIT = 4;
const int ONE_CYCLES_PER_BIT = 8;
const int SAMPLES_PER_BIT = (SAMPLE_RATE / ZERO_FREQ) * ZERO_CYCLES_PER_BIT;
const int BITS_PER_BYTE = 1 + 8 + 2;
const int AMPLITUDE = 128;
const int LEAD = 5;
const int TAIL = 5;

typedef struct WaveHeader {
  // Riff Wave Header
  char chunkId[4];
  int  chunkSize;
  char format[4];

  // Format Subchunk
  char subChunk1Id[4];
  int  subChunk1Size;
  short int audioFormat;
  short int numChannels;
  int sampleRate;
  int byteRate;
  short int blockAlign;
  short int bitsPerSample;
  //short int extraParamSize;

  // Data Subchunk
  char subChunk2Id[4];
  int  subChunk2Size;

} WaveHeader;

typedef struct Wave {
  WaveHeader header;
  char* data;
  long long int index;
  long long int size;
  long long int nSamples;
} Wave;

int isBigEndian() {
  int test = 1;
  char *p = (char*)&test;

  return p[0] == 0;
}

void reverseEndianness(const long long int size, void* value) {
  int i;
  char result[32];
  for (i = 0; i < size; i += 1) {
    result[i] = ((char*) value)[size-i-1];
  }
  for (i = 0; i < size; i += 1) {
    ((char*) value)[i] = result[i];
  }
}

void toBigEndian(const long long int size, void* value) {
  if (!isBigEndian()) {
    reverseEndianness(size, value);
  }
}

void toLittleEndian(const long long int size, void* value) {
  if (isBigEndian()) {
    reverseEndianness(size, value);
  }
}

WaveHeader makeWaveHeader() {
  WaveHeader myHeader;

  // RIFF WAVE Header
  myHeader.chunkId[0] = 'R';
  myHeader.chunkId[1] = 'I';
  myHeader.chunkId[2] = 'F';
  myHeader.chunkId[3] = 'F';
  myHeader.format[0] = 'W';
  myHeader.format[1] = 'A';
  myHeader.format[2] = 'V';
  myHeader.format[3] = 'E';

  // Format subchunk
  myHeader.subChunk1Id[0] = 'f';
  myHeader.subChunk1Id[1] = 'm';
  myHeader.subChunk1Id[2] = 't';
  myHeader.subChunk1Id[3] = ' ';
  myHeader.audioFormat = 1; // FOR PCM
  myHeader.numChannels = 1;
  myHeader.sampleRate = SAMPLE_RATE;
  myHeader.bitsPerSample = 16;
  myHeader.byteRate = myHeader.sampleRate * myHeader.bitsPerSample / 8;
  myHeader.blockAlign = myHeader.bitsPerSample / 8;

  // Data subchunk
  myHeader.subChunk2Id[0] = 'd';
  myHeader.subChunk2Id[1] = 'a';
  myHeader.subChunk2Id[2] = 't';
  myHeader.subChunk2Id[3] = 'a';

  // All sizes for later:
  // chuckSize = 4 + (8 + subChunk1Size) + (8 + subChubk2Size)
  // subChunk1Size is constanst, i'm using 16 and staying with PCM
  // subChunk2Size = nSamples * nChannels * bitsPerSample/8
  // Whenever a sample is added:
  //    chunkSize += (nChannels * bitsPerSample/8)
  //    subChunk2Size += (nChannels * bitsPerSample/8)
  myHeader.chunkSize = 4 + 8 + 16 + 8 + 0;
  myHeader.subChunk1Size = 16;
  myHeader.subChunk2Size = 0;

  return myHeader;
}

Wave makeWave() {
  Wave myWave;
  myWave.header = makeWaveHeader();
  return myWave;
}

void waveSetDuration(Wave* wave, long long int nSamples) {
  long long int totalBytes = (wave->header.blockAlign * nSamples);
  wave->data = (char*) malloc(totalBytes);
  wave->index = 0;
  wave->size = totalBytes;
  wave->nSamples = nSamples;
  wave->header.chunkSize = 4 + 8 + 16 + 8 + totalBytes;
  wave->header.subChunk2Size = totalBytes;
}

void waveDestroy(Wave* wave) {
  free(wave->data);
}

void waveAddSample(Wave* wave, const float sample) {
  int i;
  int sample16bit;
  char* sampleBytes;
  sample16bit = (int) (32767 * sample);
  //sample = (char*)&litEndianInt( sample16bit );
  toLittleEndian(2, (void*) &sample16bit);
  sampleBytes = (char*) &sample16bit;
  wave->data[wave->index + 0] = sampleBytes[0];
  wave->data[wave->index + 1] = sampleBytes[1];
  wave->index += 2;
}

int ONE_N = (SAMPLES_PER_BIT / ONE_CYCLES_PER_BIT) / 2;
void writeOne(Wave* wave) {
  for (int i = 0; i < ONE_CYCLES_PER_BIT; i++) {
    for (int j = 0; j < ONE_N; j++) {
      waveAddSample(wave, 1.0);
    }
    for (int j = 0; j < ONE_N; j++) {
      waveAddSample(wave, -1.0);
    }
  }
}

int ZERO_N = (SAMPLES_PER_BIT / ZERO_CYCLES_PER_BIT) / 2;
void writeZero(Wave* wave) {
  for (int i = 0; i < ZERO_CYCLES_PER_BIT; i++) {
    for (int j = 0; j < ZERO_N; j++) {
      waveAddSample(wave, 1.0);
    }
    for (int j = 0; j < ZERO_N; j++) {
      waveAddSample(wave, -1.0);
    }
  }
}

void waveToFile(Wave* wave, FILE *file) {
  // First make sure all numbers are little endian
  toLittleEndian(sizeof(int), (void*)&(wave->header.chunkSize));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk1Size));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.audioFormat));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.numChannels));
  toLittleEndian(sizeof(int), (void*)&(wave->header.sampleRate));
  toLittleEndian(sizeof(int), (void*)&(wave->header.byteRate));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.blockAlign));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.bitsPerSample));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk2Size));

  fwrite(&(wave->header), sizeof(WaveHeader), 1, file);
  fwrite((void*) (wave->data), sizeof(char), wave->size, file);
  fclose(file);

  // Convert back to system endian-ness
  toLittleEndian(sizeof(int), (void*)&(wave->header.chunkSize));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk1Size));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.audioFormat));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.numChannels));
  toLittleEndian(sizeof(int), (void*)&(wave->header.sampleRate));
  toLittleEndian(sizeof(int), (void*)&(wave->header.byteRate));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.blockAlign));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.bitsPerSample));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk2Size));
}

int main(int argc, char *argv[]) {
  FILE *in = fopen(argv[1], "rb");
  FILE *out = fopen(argv[2], "wb");

  fseek(in, 0L, SEEK_END);
  long int inSize = ftell(in);
  rewind(in);

  long long duration = inSize * BITS_PER_BYTE * SAMPLES_PER_BIT;
  duration += (LEAD + TAIL) * SAMPLE_RATE;

  Wave encoded = makeWave();
  waveSetDuration(&encoded, duration);
  for (int i = 0; i < LEAD * SAMPLE_RATE; i++) {
    waveAddSample(&encoded, -1.0);
  }

  for (long int i = 0; i < inSize * BITS_PER_BYTE ; i++) {
    writeZero(&encoded);
  }

  for (int i = 0; i < TAIL * SAMPLE_RATE; i++) {
    waveAddSample(&encoded, -1.0);
  }
  waveToFile(&encoded, out);
  waveDestroy(&encoded);

  char buffer[16];
  while (!feof(in)) {
    int bytesRead = fread(buffer, 1, 16, in);
    fwrite(buffer, 1, bytesRead, out);
  }

  fclose(out);
  return 0;

  return 0;
}
