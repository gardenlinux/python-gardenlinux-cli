# Push OCI artifacts cli
this tool helps you to push oci artifacts. 

## Installation
```bash
git clone https://github.com/gardenlinux/python-gardenlinux-cli.git
cd python-gardenlinux-cli
mkdir venv
python -m venv venv
source venv/bin/activate.sh
pip install -r requirements.txt
```

## Usage
The process to push a Gardenlinux build-output folder to an OCI registry is split into two steps: In the first step all files are pushed to the registry and a manifest that includes all those pushed files (layers) is created and pushed as well. An index entry that links to this manifest is created offline and written to a local file but not pushed to any index. This push to an index can be done in the second step where the local file containing the index entry is read and pushed to an index. The seperation into two steps was done because pushing of manifests takes long and writes to dedicated resources (possible to run in parallel). Updating the index on the other hand is quick but writes to a share resource (not possible to run in parallel). By splitting the process up into two steps it is possible to run the slow part in parallel and the quick part sequentially.

### 1. Push layers + manifest
To push layers you have to supply the directory with the build outputs `--dir`. Also you have to supply cname (`--cname`), architecture `--arch` and version `--version` of the build. This information will be included in the manifest. You have to supply an endpoint where the artifacts shall be pushed to `--container`, for example `ghcr.io/gardenlinux/gardenlinux`. You can disable enforced HTTPS connections to your registry with `--insecure True`. You can supply `--cosign_file <filename>` if you want to have the hash saved in `<filename>`. This can be handy to read the hash later to sign the manifest with cosign. With `--manifest_file <filename>` you tell the program in which file to store the manifests index entry. This is the file that can be used in the next step to update the index. You can use the environment variable GLOCI_REGISTRY_TOKEN to authenticate against the registry. Below is an example of a full program call of `push-manifest`
```bash
GLOCI_REGISTRY_TOKEN=asdf123 python /opt/glcli/src/glcli.py push-manifest --dir build-metal-gardener_prod --container ghcr.io/gardenlinux/gl-oci --arch amd64 --version 1592.1 --cname metal-gardener_prod --cosign_file digest --manifest_file oci_manifest_entry_metal.json
```
### 2. Update index with manifest entry
Parameters that are the same as for `push-manifest`:
* env-var `GLOCI_REGISTRY_TOKEN`
* `--version`
* `--container`
* `--manifest-file` this time this parameter adjusts the manifest entry file to be read from instead of being written to
 
A full example looks like this:
```bash
GLOCI_REGISTRY_TOKEN=asdf123 python /opt/glcli/src/glcli.py update-index --container ghcr.io/gardenlinux/gl-oci --version 1592.1 --manifest_file oci_manifest_entry_metal.json
```
