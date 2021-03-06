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
  long long int nSamples;
  FILE *file;
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
  // chuckSize = 4 + (8 + subChunk1Size) + (8 + subChunk2Size)
  // subChunk1Size is constanst, i'm using 16 and staying with PCM
  // subChunk2Size = nSamples * nChannels * bitsPerSample/8
  // Whenever a sample is added:
  //    chunkSize += (nChannels * bitsPerSample/8)
  //    subChunk2Size += (nChannels * bitsPerSample/8)
  myHeader.subChunk1Size = 16;
  myHeader.subChunk2Size = 0;
  myHeader.chunkSize = 4 + 8 + myHeader.subChunk1Size + 8 + myHeader.subChunk2Size;

  return myHeader;
}

Wave makeWave(FILE *file) {
  Wave myWave;
  myWave.header = makeWaveHeader();
  myWave.file = file;
  myWave.nSamples = 0;
  return myWave;
}

void waveAddSample(Wave* wave, const float sample) {
  int sample16bit;
  char* sampleBytes;
  sample16bit = (int) (32767 * sample);
  //sample = (char*)&litEndianInt( sample16bit );
  toLittleEndian(2, (void*) &sample16bit);
  sampleBytes = (char*) &sample16bit;
  fwrite(sampleBytes, 1, 2, wave->file);
  wave->nSamples++;
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

void waveWriteHeader(Wave *wave) {
  wave->header.subChunk2Size = wave->nSamples * (wave->header.bitsPerSample / 8);
  wave->header.chunkSize = 4 + 8 + wave->header.subChunk1Size + 8 + wave->header.subChunk2Size;

  long pos = ftell(wave->file);
  rewind(wave->file);

  toLittleEndian(sizeof(int), (void*)&(wave->header.chunkSize));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk1Size));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.audioFormat));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.numChannels));
  toLittleEndian(sizeof(int), (void*)&(wave->header.sampleRate));
  toLittleEndian(sizeof(int), (void*)&(wave->header.byteRate));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.blockAlign));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.bitsPerSample));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk2Size));

  fwrite(&(wave->header), sizeof(WaveHeader), 1, wave->file);

  toLittleEndian(sizeof(int), (void*)&(wave->header.chunkSize));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk1Size));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.audioFormat));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.numChannels));
  toLittleEndian(sizeof(int), (void*)&(wave->header.sampleRate));
  toLittleEndian(sizeof(int), (void*)&(wave->header.byteRate));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.blockAlign));
  toLittleEndian(sizeof(short int), (void*)&(wave->header.bitsPerSample));
  toLittleEndian(sizeof(int), (void*)&(wave->header.subChunk2Size));

  fseek(wave->file, pos, SEEK_SET);
}

int main(int argc, char *argv[]) {
  FILE *in = fopen(argv[1], "rb");
  FILE *out = fopen(argv[2], "wb");

  Wave encoded = makeWave(out);
  waveWriteHeader(&encoded);

  for (int i = 0; i < LEAD * SAMPLE_RATE; i++) {
    waveAddSample(&encoded, -1.0);
  }

  writeOne(&encoded);
  writeZero(&encoded);

  for (int i = 0; i < TAIL * SAMPLE_RATE; i++) {
    waveAddSample(&encoded, -1.0);
  }

  waveWriteHeader(&encoded);
  fclose(in);
  fclose(out);

  return 0;
}
