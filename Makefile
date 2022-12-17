update-proto:
	git fetch proto main
	git subtree pull --prefix proto/ proto main --squash

set-proto:
	git remote add -f proto git@github.com:asuyou/anzen-proto.git
	git subtree add --prefix proto/ proto main --squash

build-proto:
	fd . proto/anzen/v1 -e proto --color=never | xargs python -m grpc_tools.protoc \
	-I ./proto/ \
	--proto_path=./proto/anzen/v1 \
	--python_out=./src/ \
	--pyi_out=./src/ \
	--grpc_python_out=./src/ \

