# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, cloverstd (https://gist.github.com/cloverstd/10712505)
# Copyright (c) 2018, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
#  for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new
import functools


def cache(expires=7200):
    def _func(func):
        @functools.wraps(func)
        def wrapper(handler, *args, **kwargs):
            handler.expires = expires
            return func(handler, *args, **kwargs)
        return wrapper
    return _func


class CacheMixin(object):

    @property
    def cache(self):
        return self.application.cache

    async def prepare(self):
        super(CacheMixin, self).prepare()
        key = self._generate_key(self.request)
        if await self.cache.exists(self._prefix(key)):
            rv = pickle.loads(await self.cache.get(self._prefix(key)))
            self.write_cache(rv)
            self.finish()

    def _generate_key(self, request):
        key = pickle.dumps((request.path, request.arguments))
        return sha1(key).hexdigest()

    def _prefix(self, key):
        return 'Cache:%s' % key

    def write_cache(self, chunk):
        super(CacheMixin, self).write(chunk)

    async def write(self, chunk):
        pickled = pickle.dumps(chunk)
        key = self._generate_key(self.request)
        if hasattr(self, 'expires'):
            await self.cache.set(self._prefix(key), pickled, self.expires)
        else:
            await self.cache.set(self._prefix(key), pickled)
        super(CacheMixin, self).write(chunk)


class CacheBackend(object):
    '''
    The base Cache Backend class
    '''

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, timeout):
        raise NotImplementedError

    def delitem(self, key):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError


class RedisCacheBackend(CacheBackend):

    def __init__(self, redis_connection, **options):
        self.options = dict(timeout=86400)
        self.options.update(options)
        self.redis = redis_connection

    async def get(self, key):
        if await self.exists(key):
            return await self.redis.get(key)
        return None

    async def set(self, key, value, timeout=None):
        await self.redis.set(key, value)
        if timeout:
            await self.redis.expire(key, timeout)
        else:
            await self.redis.expire(key, self.options['timeout'])

    async def delitem(self, key):
        await self.redis.delete(key)

    async def exists(self, key):
        return bool(await self.redis.exists(key))
