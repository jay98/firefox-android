# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Apply some defaults and minor modifications to the tasks defined in the build
kind.
"""


from taskgraph.transforms.base import TransformSequence
from taskgraph.util.schema import resolve_keyed_by


transforms = TransformSequence()


@transforms.add
def resolve_keys(config, tasks):
    for task in tasks:
        for key in ("scopes", "treeherder.symbol"):
            resolve_keyed_by(
                task,
                key,
                item_name=task["name"],
                **{
                    'build-type': task["attributes"]["build-type"],
                    'level': config.params["level"],
                }
            )
        yield task


@transforms.add
def make_task_description(config, tasks):
    for task in tasks:
        product = "Firefox-android"  # shipit exactly uses this case
        # {ver} is just a magic string to show "this isn't right"
        # https://github.com/mozilla-mobile/fenix/pull/7306/files#r360248631
        version = config.params['version'] or "{ver}"
        task['worker']['release-name'] = '{product}-{version}-build{build_number}'.format(
            product=product,
            version=version,
            build_number=config.params.get('build_number', 1)
        )
        yield task
