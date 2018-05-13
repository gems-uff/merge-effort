#!/usr/bin/env bash
curl --user ${CIRCLE_TOKEN}: \
    --request POST \
    --form revision=30a9596316d9852b88b39cb0e213a014597d4625\
    --form config=@config.yml \
    --form notify=false \
        https://circleci.com/api/v1.1/project/github/gems-uff/merge-effort/tree/master
