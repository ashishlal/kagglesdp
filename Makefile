data/sample_submission.7z:
	wget -x --load-cookies data/cookies.txt https://www.kaggle.com/c/porto-seguro-safe-driver-prediction/download/sample_submission.7z -O data/sample_submission.7z --continue

data/test.7z:
	wget -x --load-cookies data/cookies.txt https://www.kaggle.com/c/porto-seguro-safe-driver-prediction/download/test.7z -O data/test.7z --continue

data/train.7z:
	wget -x --load-cookies data/cookies.txt https://www.kaggle.com/c/porto-seguro-safe-driver-prediction/download/train.7z -O data/train.7z --continue

data: data/sample_submission.7z data/test.7z data/train.7z

clean: 
	rm -rf data/*.7z

.PHONY: data

