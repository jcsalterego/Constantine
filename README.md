# Constantine

Constantine helps you find your posts in the [Hellthread](https://github.com/bluesky-social/atproto/pull/988/files).

## Requirements

- Python 3
- Bluesky Social account

## Usage

Set environment variables `BLUESKY_USER` and `BLUESKY_APP_PASSWORD`.

Example:

```
export BLUESKY_USER=jcsalterego.bsky.social
export BLUESKY_APP_PASSWORD=abcd-efgh-ijkl-mnop
./get-hellthreads.py jcsalterego.bsky.social
```
```
cursor = 1687536512998::bafyreid6a6vn7romdf5tosqgx55qu4cjktq75dho53wyfh64rmdmacvhfe
cursor = 1687453339465::bafyreidzvrmzhqypkgqij5wqpcpcu3tvhg4nalaryesocpy5njbfnfevsq
<snip>
cursor = 1682543089140::bafyreieulju52qkz67oqlanpdgt3jw7ahpdbkmo6sn62ngszi3rn6pn4ne
cursor = 1672610718852::bafyreiff6tetdt34qlbg75sn62ptaiaoiyyjbyyrrbnmumkkkphfcxpnge
2835 posts total
10 hellthread posts total
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxr33lcv552e
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxr2bsxbob2n
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxoseuz45i2e
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxos3vem752w
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxorzy2f6n2w
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxk5sj7ppe23
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jxgjimt4ye2n
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jwxxzhdrc22u
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jwxwrb2g7c2b
https://bsky.app/profile/did:plc:vc7f4oafdgxsihk4cry2xpze/post/3jvrw74c26r2b
```

## LICENSE

[2-Clause BSD](LICENSE)
