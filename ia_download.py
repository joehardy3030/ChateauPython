import internetarchive as ia


def download_show(id):
    s = ia.get_session()
    s.mount_http_adapter()
    s_item = s.get_item(id)
    #s_item.metadata

    fnames = [f.name for f in s_item.get_files(id, glob_pattern='*mp3')]
    for f in fnames:
        s_item.download(f, destdir="downloads")


if __name__ == "__main__":
    id = 'gd70-02-11.early-late.sbd.sacks.90.sbefail.shnf'
    download_show(id=id)
