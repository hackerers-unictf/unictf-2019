#!/bin/bash
if [ -z "$1" ]; then
    echo "Supply virtual disk format (vmdk, vdi or qcow2)"
    echo "Please note that vmdk is for vmware, vdi for virtualbox and qcow2 for kvm-qemu"
    exit 1
fi
check=0
if [ "$1" != "qcow2" ]; then
    check=$(( check + 1 ))
fi
if [ "$1" != "vdi" ]; then
    check=$(( check + 1 ))
fi
if [ "$1" != "vmdk" ]; then
    check=$(( check + 1 ))
fi

#echo $check

if [ $check -eq 3 ]; then
    echo "This format doesn't exists or isn't supported (please use vmdk, vdi or qcow2)"
    echo "Please note that vmdk is for vmware, vdi for virtualbox and qcow2 for kvm-qemu"
    exit 1
fi

echo "Intalling qemu-utils and 7zip..."
sudo apt install qemu-utils p7zip-full megatools -y
echo "Done."
echo " "
echo "Downloading VMs"
echo " "
megadl https://mega.nz/#!oxNBCC5T!flmB8CjHLWUyHRqXN5kHKZqFi3fgN0hDZVKuv0-ALBc

echo "Extracting disk images, please be patient."
7z x ./VMs_uniCTf19.7z

if [ "$1" == "vmdk" ] || [ "$1" == "vdi" ]; then
    echo "Converting disk image to the chosen format, please be patient."
    qemu-img convert -f qcow2 ./Arbitro.qcow -O $1 ./Arbitro.$1
    qemu-img convert -f qcow2 ./BOFT1.qcow -O $1 ./BOFT1.$1
    qemu-img convert -f qcow2 ./BOFT2.qcow -O $1 ./BOFT2.$1
    qemu-img convert -f qcow2 ./PalioT1.qcow -O $1 ./PalioT1.$1
    qemu-img convert -f qcow2 ./PalioT2.qcow -O $1 ./PalioT2.$1
    echo "Done"
    exit 0
fi

if [ "$1" == "qcow2" ]; then
    echo "Already in the right format! Nothing to do! Bye"
    exit 0
fi
