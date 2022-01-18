#!/usr/bin/python3

# Copyright (C) 2022  OX Software GmbH
#                     Wolfgang Rosenauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from zeep import Client
import settings
import argparse


def main():
    parser = argparse.ArgumentParser(description='Lists catchall target of an OX Cloud domain context.')
    parser.add_argument("-n", dest="context_name",
                        help="Context name to list.")
    parser.add_argument(
        "-c", "--cid", help="Context ID to list.", type=int)
    args = parser.parse_args()

    if args.context_name is None and args.cid is None:
        parser.error("Context must be specified by either -n or -c !")

    ctx = {}
    if args.cid is not None:
        ctx["id"] = args.cid
    else:
        ctx["name"] = settings.getCreds()["login"] + "_" + args.context_name

    contextService = Client(settings.getHost()+"OXResellerContextService?wsdl")
    ctx = contextService.service.getData(ctx, settings.getCreds())

    oxaasService = Client(settings.getHost()+"OXaaSService?wsdl")

    catchalls = oxaasService.service.listDomainCatchalls(ctx.id, settings.getCreds())

    print (catchalls)

if __name__ == "__main__":
    main()