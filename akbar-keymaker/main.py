from Crypto.PublicKey import RSA


def normalize_private_key_format(pk: str) -> str:
    return pk.replace("RSA PRIVATE KEY", "PRIVATE KEY")


def main():
    data = RSA.generate(2048)
    private_key = normalize_private_key_format(data.exportKey().decode())
    public_key = data.public_key().exportKey().decode()
    output = f"{public_key}\n{private_key}"
    with open("pair.pem", "w") as f:
        f.write(output)


if __name__ == '__main__':
    main()
