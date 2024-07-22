from bs4 import BeautifulSoup
import requests
# import unicodedata

def is_palm_orientation_class(char):
    if '\uE038' <= char <= '\uE03F': # E038 is unicode char
        return ord(char) - ord('\uE038') # difference gives class number [0,7]
    else:
        return None
    # """
    # ^^^ checking if a given character falls within the Hamnosys unicode range of E038 to E03F,
    # which corresponds to palm orientation classes.
    # """
    # return '\uE038' <= char <= '\uE03F'

with open('annotations.txt', 'a') as f:
    for i in range(11, 13):
        url = f'https://www.slownikpjm.uw.edu.pl/en/gloss/view/{i}'

    # page = requests.get(url).text
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'lxml')

    # hamanns = soup.find('span', class_='videocontent_main_hamnosyseditor').text
    # formatted = unicodedata.normalize('NFKD', hamanns).encode('ascii', 'ignore').decode('utf-8')
    # print(hamanns)

        video = soup.find('video', {'id': 'gloss_view_video'})
        if video:
            source = video.find('source')
            video = "https://www.slownikpjm.uw.edu.pl" + source['src']
        else:
            video = 'no video'

        hamnosys = soup.find('span', {'class': 'videocontent_main_hamnosyseditor'})

        if hamnosys:
            hamnosys = hamnosys.text.strip()
        else:
            hamnosys = 'no HamNoSys'

        # palm_orientation_class = ''
        for char in hamnosys:
            palm_orientation_class = is_palm_orientation_class(char)
            if palm_orientation_class is not None:
                break
            # if is_palm_orientation_class(char):
            #     palm_orientation_class = char
            #     break

        print(f'Page {i}:')
        print('Video:', video)
        print('HamNoSys:', hamnosys)
        print('Palm orientation class:', palm_orientation_class)
        print()

        f.write(f'Page {i}:\n')
        f.write(f'HamNoSys: {hamnosys}\n')
        f.write(f'Palm orientation class: {palm_orientation_class}\n')
        f.write('\n')
        
        # downloading the video:
        if video != 'no video':
            r = requests.get(video, stream=True)
            video_path = f'videos/video_{i}.mp4'
            with open(video_path, 'wb') as vf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        vf.write(chunk)