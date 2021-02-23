OBJDIR=obj

CC=gcc
LD=ld
CFLAGS=-std=c11
LDSTATIC = $(shell libpng-config --ldflags )

_OBJS = p8png.o

ifdef RELEASE
DEFS += -xSSE3 -O3 -DNDEBUG
else
DEFS += -g
endif

all: p8png
	@echo "building cart"
	./p8png cart.p8.png cart_image.png 1000words.png
	exiv2 -m exif.txt 1000words.png
	mv 1000words.png ../dist

OBJS = $(patsubst %,$(OBJDIR)/%,$(_OBJS))

p8png: $(OBJS)
	$(CC) -o $@ $^ $(LDSTATIC)

$(OBJDIR)/%.o: %.c $(OBJDIR)
	$(CC) -c -o $@ $< $(CFLAGS) $(DEFS)

$(OBJDIR):
	mkdir $(OBJDIR)

clean:
	rm -rf $(OBJDIR)/*.o p8png

.PHONY: all
