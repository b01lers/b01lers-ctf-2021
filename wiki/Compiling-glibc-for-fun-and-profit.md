`glibc` is actually shockingly easy to compile, but there are a couple things that need to be written down to make them easier to remember.All of 

## Compiling glibc for x86_64:

```
# Clone libc
git clone ssh://git@github.com/bminor/glibc
cd glibc
git checkout <commit_you_need>
cd ..

# Create a build directory
mkdir build && cd build

# For standard builds, this is all you need
../configure --prefix=$(pwd)
make -j9
```

## Compiling glibc for x32:

This is a lot trickier on a 64-bit machine. I use a docker container to do it. 

```
cat > Dockerfile <<< "
FROM i386/ubuntu:latest

RUN apt -y update
RUN apt -y install gawk bison python3 flex linux-headers-generic grep build-essential
COPY glibc /opt/glibc
RUN cd /opt/glibc && \
    rm -rf build && \
    mkdir -p build && \
    cd build && ../configure --prefix=$(pwd) --libdir=$(pwd)/lib --libexecdir=$(pwd)/lib --enable-multi-arch \
                    --enable-stack-protector=strong CC="gcc -m32" CXX="g++ -m32" \
                     CFLAGS="-O2 -march=i686" \
                     CXXFLAGS="-O2 -march=i686" \
                     i686-linux-gnu && \
    make"
git clone ssh://git@github.com/bminor/glibc
cd glibc
git checkout <your_desired_commit>
cd ..
docker build -t glibc-builder-x86 .
id=$(docker create glibc-builder-x86:latest)
docker cp $id:/opt/glibc/build - > build.tar
docker rm -v $id
```