all:
	python3 gen_flag.py
	cargo build --release
	cp ./target/release/scrapyard_scramble ../dist

clean:
	- rm src/flag.enc
	- cargo clean
	- rm ../dist/scrapyard_scramble
	- rm Cargo.lock
