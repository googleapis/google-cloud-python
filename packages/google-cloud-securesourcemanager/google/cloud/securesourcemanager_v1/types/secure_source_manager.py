# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securesourcemanager.v1",
    manifest={
        "Instance",
        "Repository",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "GetInstanceRequest",
        "CreateInstanceRequest",
        "DeleteInstanceRequest",
        "OperationMetadata",
        "ListRepositoriesRequest",
        "ListRepositoriesResponse",
        "GetRepositoryRequest",
        "CreateRepositoryRequest",
        "DeleteRepositoryRequest",
    },
)


class Instance(proto.Message):
    r"""A resource that represents a Secure Source Manager instance.

    Attributes:
        name (str):
            Optional. A unique identifier for an instance. The name
            should be of the format:
            ``projects/{project_number}/locations/{location_id}/instances/{instance_id}``

            ``project_number``: Maps to a unique int64 id assigned to
            each project.

            ``location_id``: Refers to the region where the instance
            will be deployed. Since Secure Source Manager is a regional
            service, it must be one of the valid GCP regions.

            ``instance_id``: User provided name for the instance, must
            be unique for a project_number and location_id combination.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update timestamp.
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs.
        private_config (google.cloud.securesourcemanager_v1.types.Instance.PrivateConfig):
            Optional. Private settings for private
            instance.
        state (google.cloud.securesourcemanager_v1.types.Instance.State):
            Output only. Current state of the instance.
        state_note (google.cloud.securesourcemanager_v1.types.Instance.StateNote):
            Output only. An optional field providing
            information about the current instance state.
        kms_key (str):
            Optional. Immutable. Customer-managed encryption key name,
            in the format
            projects/\ */locations/*/keyRings/*/cryptoKeys/*.
        host_config (google.cloud.securesourcemanager_v1.types.Instance.HostConfig):
            Output only. A list of hostnames for this
            instance.
    """

    class State(proto.Enum):
        r"""Secure Source Manager instance state.

        Values:
            STATE_UNSPECIFIED (0):
                Not set. This should only be the case for
                incoming requests.
            CREATING (1):
                Instance is being created.
            ACTIVE (2):
                Instance is ready.
            DELETING (3):
                Instance is being deleted.
            PAUSED (4):
                Instance is paused.
            UNKNOWN (6):
                Instance is unknown, we are not sure if it's
                functioning.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        DELETING = 3
        PAUSED = 4
        UNKNOWN = 6

    class StateNote(proto.Enum):
        r"""Provides information about the current instance state.

        Values:
            STATE_NOTE_UNSPECIFIED (0):
                STATE_NOTE_UNSPECIFIED as the first value of State.
            PAUSED_CMEK_UNAVAILABLE (1):
                CMEK access is unavailable.
            INSTANCE_RESUMING (2):
                INSTANCE_RESUMING indicates that the instance was previously
                paused and is under the process of being brought back.
        """
        STATE_NOTE_UNSPECIFIED = 0
        PAUSED_CMEK_UNAVAILABLE = 1
        INSTANCE_RESUMING = 2

    class HostConfig(proto.Message):
        r"""HostConfig has different instance endpoints.

        Attributes:
            html (str):
                Output only. HTML hostname.
            api (str):
                Output only. API hostname. This is the hostname to use for
                **Host: Data Plane** endpoints.
            git_http (str):
                Output only. Git HTTP hostname.
            git_ssh (str):
                Output only. Git SSH hostname.
        """

        html: str = proto.Field(
            proto.STRING,
            number=1,
        )
        api: str = proto.Field(
            proto.STRING,
            number=2,
        )
        git_http: str = proto.Field(
            proto.STRING,
            number=3,
        )
        git_ssh: str = proto.Field(
            proto.STRING,
            number=4,
        )

    class PrivateConfig(proto.Message):
        r"""PrivateConfig includes settings for private instance.

        Attributes:
            is_private (bool):
                Required. Immutable. Indicate if it's private
                instance.
            ca_pool (str):
                Required. Immutable. CA pool resource, resource must in the
                format of
                ``projects/{project}/locations/{location}/caPools/{ca_pool}``.
            http_service_attachment (str):
                Output only. Service Attachment for HTTP, resource is in the
                format of
                ``projects/{project}/regions/{region}/serviceAttachments/{service_attachment}``.
            ssh_service_attachment (str):
                Output only. Service Attachment for SSH, resource is in the
                format of
                ``projects/{project}/regions/{region}/serviceAttachments/{service_attachment}``.
        """

        is_private: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        ca_pool: str = proto.Field(
            proto.STRING,
            number=2,
        )
        http_service_attachment: str = proto.Field(
            proto.STRING,
            number=3,
        )
        ssh_service_attachment: str = proto.Field(
            proto.STRING,
            number=4,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    private_config: PrivateConfig = proto.Field(
        proto.MESSAGE,
        number=13,
        message=PrivateConfig,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    state_note: StateNote = proto.Field(
        proto.ENUM,
        number=10,
        enum=StateNote,
    )
    kms_key: str = proto.Field(
        proto.STRING,
        number=11,
    )
    host_config: HostConfig = proto.Field(
        proto.MESSAGE,
        number=9,
        message=HostConfig,
    )


class Repository(proto.Message):
    r"""Metadata of a Secure Source Manager repository.

    Attributes:
        name (str):
            Optional. A unique identifier for a repository. The name
            should be of the format:
            ``projects/{project}/locations/{location_id}/repositories/{repository_id}``
        description (str):
            Optional. Description of the repository,
            which cannot exceed 500 characters.
        instance (str):
            Optional. The name of the instance in which the repository
            is hosted, formatted as
            ``projects/{project_number}/locations/{location_id}/instances/{instance_id}``
            For data plane CreateRepository requests, this field is
            output only. For control plane CreateRepository requests,
            this field is used as input.
        uid (str):
            Output only. Unique identifier of the
            repository.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update timestamp.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        uris (google.cloud.securesourcemanager_v1.types.Repository.URIs):
            Output only. URIs for the repository.
        initial_config (google.cloud.securesourcemanager_v1.types.Repository.InitialConfig):
            Input only. Initial configurations for the
            repository.
    """

    class URIs(proto.Message):
        r"""URIs for the repository.

        Attributes:
            html (str):
                Output only. HTML is the URI for user to view
                the repository in a browser.
            git_https (str):
                Output only. git_https is the git HTTPS URI for git
                operations.
            api (str):
                Output only. API is the URI for API access.
        """

        html: str = proto.Field(
            proto.STRING,
            number=1,
        )
        git_https: str = proto.Field(
            proto.STRING,
            number=2,
        )
        api: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class InitialConfig(proto.Message):
        r"""Repository initialization configuration.

        Attributes:
            default_branch (str):
                Default branch name of the repository.
            gitignores (MutableSequence[str]):
                List of gitignore template names user can
                choose from. Valid values: actionscript, ada,
                agda, android, anjuta, ansible,
                appcelerator-titanium, app-engine, archives,
                arch-linux-packages, atmel-studio, autotools,
                backup, bazaar, bazel, bitrix, bricx-cc, c,
                cake-php, calabash, cf-wheels, chef-cookbook,
                clojure, cloud9, c-make, code-igniter, code-kit,
                code-sniffer, common-lisp, composer, concrete5,
                coq, cordova, cpp, craft-cms, cuda, cvs, d,
                dart, dart-editor, delphi, diff, dm,
                dreamweaver, dropbox, drupal, drupal-7, eagle,
                eclipse, eiffel-studio, elisp, elixir, elm,
                emacs, ensime, epi-server, erlang, esp-idf,
                espresso, exercism, expression-engine, ext-js,
                fancy, finale, flex-builder, force-dot-com,
                fortran, fuel-php, gcov, git-book,
                gnome-shell-extension, go, godot, gpg, gradle,
                grails, gwt, haskell, hugo, iar-ewarm, idris,
                igor-pro, images, infor-cms, java, jboss,
                jboss-4, jboss-6, jdeveloper, jekyll,
                jenkins-home, jenv, jet-brains, jigsaw, joomla,
                julia, jupyter-notebooks, kate, kdevelop4,
                kentico, ki-cad, kohana, kotlin, lab-view,
                laravel, lazarus, leiningen, lemon-stand,
                libre-office, lilypond, linux, lithium, logtalk,
                lua, lyx, mac-os, magento, magento-1, magento-2,
                matlab, maven, mercurial, mercury, metals,
                meta-programming-system, meteor,
                microsoft-office, model-sim, momentics,
                mono-develop, nanoc, net-beans, nikola, nim,
                ninja, node, notepad-pp, nwjs, objective--c,
                ocaml, octave, opa, open-cart, openssl,
                oracle-forms, otto, packer, patch, perl, perl6,
                phalcon, phoenix, pimcore, play-framework,
                plone, prestashop, processing, psoc-creator,
                puppet, pure-script, putty, python, qooxdoo, qt,
                r, racket, rails, raku, red, redcar, redis,
                rhodes-rhomobile, ros, ruby, rust, sam, sass,
                sbt, scala, scheme, scons, scrivener, sdcc,
                seam-gen, sketch-up, slick-edit, smalltalk,
                snap, splunk, stata, stella, sublime-text,
                sugar-crm, svn, swift, symfony, symphony-cms,
                synopsys-vcs, tags, terraform, tex, text-mate,
                textpattern, think-php, tortoise-git,
                turbo-gears-2, typo3, umbraco, unity,
                unreal-engine, vagrant, vim, virtual-env,
                virtuoso, visual-studio, visual-studio-code,
                vue, vvvv, waf, web-methods, windows,
                word-press, xcode, xilinx, xilinx-ise, xojo,
                yeoman, yii, zend-framework, zephir.
            license_ (str):
                License template name user can choose from.
                Valid values: license-0bsd,
                license-389-exception, aal, abstyles,
                adobe-2006, adobe-glyph, adsl, afl-1-1, afl-1-2,
                afl-2-0, afl-2-1, afl-3-0, afmparse, agpl-1-0,
                agpl-1-0-only, agpl-1-0-or-later, agpl-3-0-only,
                agpl-3-0-or-later, aladdin, amdplpa, aml, ampas,
                antlr-pd, antlr-pd-fallback, apache-1-0,
                apache-1-1, apache-2-0, apafml, apl-1-0,
                apsl-1-0, apsl-1-1, apsl-1-2, apsl-2-0,
                artistic-1-0, artistic-1-0-cl8,
                artistic-1-0-perl, artistic-2-0,
                autoconf-exception-2-0, autoconf-exception-3-0,
                bahyph, barr, beerware, bison-exception-2-2,
                bittorrent-1-0, bittorrent-1-1, blessing,
                blueoak-1-0-0, bootloader-exception, borceux,
                bsd-1-clause, bsd-2-clause,
                bsd-2-clause-freebsd, bsd-2-clause-netbsd,
                bsd-2-clause-patent, bsd-2-clause-views,
                bsd-3-clause, bsd-3-clause-attribution,
                bsd-3-clause-clear, bsd-3-clause-lbnl,
                bsd-3-clause-modification,
                bsd-3-clause-no-nuclear-license,
                bsd-3-clause-no-nuclear-license-2014,
                bsd-3-clause-no-nuclear-warranty,
                bsd-3-clause-open-mpi, bsd-4-clause,
                bsd-4-clause-shortened, bsd-4-clause-uc,
                bsd-protection, bsd-source-code, bsl-1-0,
                busl-1-1, cal-1-0,
                cal-1-0-combined-work-exception, caldera,
                catosl-1-1, cc0-1-0, cc-by-1-0, cc-by-2-0,
                cc-by-3-0, cc-by-3-0-at, cc-by-3-0-us,
                cc-by-4-0, cc-by-nc-1-0, cc-by-nc-2-0,
                cc-by-nc-3-0, cc-by-nc-4-0, cc-by-nc-nd-1-0,
                cc-by-nc-nd-2-0, cc-by-nc-nd-3-0,
                cc-by-nc-nd-3-0-igo, cc-by-nc-nd-4-0,
                cc-by-nc-sa-1-0, cc-by-nc-sa-2-0,
                cc-by-nc-sa-3-0, cc-by-nc-sa-4-0, cc-by-nd-1-0,
                cc-by-nd-2-0, cc-by-nd-3-0, cc-by-nd-4-0,
                cc-by-sa-1-0, cc-by-sa-2-0, cc-by-sa-2-0-uk,
                cc-by-sa-2-1-jp, cc-by-sa-3-0, cc-by-sa-3-0-at,
                cc-by-sa-4-0, cc-pddc, cddl-1-0, cddl-1-1,
                cdla-permissive-1-0, cdla-sharing-1-0,
                cecill-1-0, cecill-1-1, cecill-2-0, cecill-2-1,
                cecill-b, cecill-c, cern-ohl-1-1, cern-ohl-1-2,
                cern-ohl-p-2-0, cern-ohl-s-2-0, cern-ohl-w-2-0,
                clartistic, classpath-exception-2-0,
                clisp-exception-2-0, cnri-jython, cnri-python,
                cnri-python-gpl-compatible, condor-1-1,
                copyleft-next-0-3-0, copyleft-next-0-3-1,
                cpal-1-0, cpl-1-0, cpol-1-02, crossword,
                crystal-stacker, cua-opl-1-0, cube, c-uda-1-0,
                curl, d-fsl-1-0, diffmark,
                digirule-foss-exception, doc, dotseqn, drl-1-0,
                dsdp, dvipdfm, ecl-1-0, ecl-2-0,
                ecos-exception-2-0, efl-1-0, efl-2-0, egenix,
                entessa, epics, epl-1-0, epl-2-0, erlpl-1-1,
                etalab-2-0, eu-datagrid, eupl-1-0, eupl-1-1,
                eupl-1-2, eurosym, fair,
                fawkes-runtime-exception, fltk-exception,
                font-exception-2-0, frameworx-1-0, freebsd-doc,
                freeimage, freertos-exception-2-0, fsfap, fsful,
                fsfullr, ftl, gcc-exception-2-0,
                gcc-exception-3-1, gd, gfdl-1-1-invariants-only,
                gfdl-1-1-invariants-or-later,
                gfdl-1-1-no-invariants-only,
                gfdl-1-1-no-invariants-or-later, gfdl-1-1-only,
                gfdl-1-1-or-later, gfdl-1-2-invariants-only,
                gfdl-1-2-invariants-or-later,
                gfdl-1-2-no-invariants-only,
                gfdl-1-2-no-invariants-or-later, gfdl-1-2-only,
                gfdl-1-2-or-later, gfdl-1-3-invariants-only,
                gfdl-1-3-invariants-or-later,
                gfdl-1-3-no-invariants-only,
                gfdl-1-3-no-invariants-or-later, gfdl-1-3-only,
                gfdl-1-3-or-later, giftware, gl2ps, glide,
                glulxe, glwtpl, gnu-javamail-exception, gnuplot,
                gpl-1-0-only, gpl-1-0-or-later, gpl-2-0-only,
                gpl-2-0-or-later, gpl-3-0-linking-exception,
                gpl-3-0-linking-source-exception, gpl-3-0-only,
                gpl-3-0-or-later, gpl-cc-1-0, gsoap-1-3b,
                haskell-report, hippocratic-2-1, hpnd,
                hpnd-sell-variant, htmltidy,
                i2p-gpl-java-exception, ibm-pibs, icu, ijg,
                image-magick, imatix, imlib2, info-zip, intel,
                intel-acpi, interbase-1-0, ipa, ipl-1-0, isc,
                jasper-2-0, jpnic, json, lal-1-2, lal-1-3,
                latex2e, leptonica, lgpl-2-0-only,
                lgpl-2-0-or-later, lgpl-2-1-only,
                lgpl-2-1-or-later, lgpl-3-0-linking-exception,
                lgpl-3-0-only, lgpl-3-0-or-later, lgpllr,
                libpng, libpng-2-0, libselinux-1-0, libtiff,
                libtool-exception, liliq-p-1-1, liliq-r-1-1,
                liliq-rplus-1-1, linux-openib,
                linux-syscall-note, llvm-exception, lpl-1-0,
                lpl-1-02, lppl-1-0, lppl-1-1, lppl-1-2,
                lppl-1-3a, lppl-1-3c, lzma-exception,
                make-index, mif-exception, miros, mit, mit-0,
                mit-advertising, mit-cmu, mit-enna, mit-feh,
                mit-modern-variant, mitnfa, mit-open-group,
                motosoto, mpich2, mpl-1-0, mpl-1-1, mpl-2-0,
                mpl-2-0-no-copyleft-exception, ms-pl, ms-rl,
                mtll, mulanpsl-1-0, mulanpsl-2-0, multics, mup,
                naist-2003, nasa-1-3, naumen, nbpl-1-0,
                ncgl-uk-2-0, ncsa, netcdf, net-snmp, newsletr,
                ngpl, nist-pd, nist-pd-fallback, nlod-1-0, nlpl,
                nokia, nokia-qt-exception-1-1, nosl, noweb,
                npl-1-0, npl-1-1, nposl-3-0, nrl, ntp, ntp-0,
                ocaml-lgpl-linking-exception,
                occt-exception-1-0, occt-pl, oclc-2-0, odbl-1-0,
                odc-by-1-0, ofl-1-0, ofl-1-0-no-rfn,
                ofl-1-0-rfn, ofl-1-1, ofl-1-1-no-rfn,
                ofl-1-1-rfn, ogc-1-0, ogdl-taiwan-1-0,
                ogl-canada-2-0, ogl-uk-1-0, ogl-uk-2-0,
                ogl-uk-3-0, ogtsl, oldap-1-1, oldap-1-2,
                oldap-1-3, oldap-1-4, oldap-2-0, oldap-2-0-1,
                oldap-2-1, oldap-2-2, oldap-2-2-1, oldap-2-2-2,
                oldap-2-3, oldap-2-4, oldap-2-7, oml,
                openjdk-assembly-exception-1-0, openssl,
                openvpn-openssl-exception, opl-1-0, oset-pl-2-1,
                osl-1-0, osl-1-1, osl-2-0, osl-2-1, osl-3-0,
                o-uda-1-0, parity-6-0-0, parity-7-0-0, pddl-1-0,
                php-3-0, php-3-01, plexus,
                polyform-noncommercial-1-0-0,
                polyform-small-business-1-0-0, postgresql,
                psf-2-0, psfrag,
                ps-or-pdf-font-exception-20170817, psutils,
                python-2-0, qhull, qpl-1-0,
                qt-gpl-exception-1-0, qt-lgpl-exception-1-1,
                qwt-exception-1-0, rdisc, rhecos-1-1, rpl-1-1,
                rpsl-1-0, rsa-md, rscpl, ruby, saxpath, sax-pd,
                scea, sendmail, sendmail-8-23, sgi-b-1-0,
                sgi-b-1-1, sgi-b-2-0, shl-0-51, shl-2-0,
                shl-2-1, simpl-2-0, sissl, sissl-1-2, sleepycat,
                smlnj, smppl, snia, spencer-86, spencer-94,
                spencer-99, spl-1-0, ssh-openssh, ssh-short,
                sspl-1-0, sugarcrm-1-1-3, swift-exception, swl,
                tapr-ohl-1-0, tcl, tcp-wrappers, tmate,
                torque-1-1, tosl, tu-berlin-1-0, tu-berlin-2-0,
                u-boot-exception-2-0, ucl-1-0, unicode-dfs-2015,
                unicode-dfs-2016, unicode-tou,
                universal-foss-exception-1-0, unlicense,
                upl-1-0, vim, vostrom, vsl-1-0, w3c,
                w3c-19980720, w3c-20150513, watcom-1-0, wsuipa,
                wtfpl, wxwindows-exception-3-1, x11, xerox,
                xfree86-1-1, xinetd, xnet, xpp, xskat, ypl-1-0,
                ypl-1-1, zed, zend-2-0, zimbra-1-3, zimbra-1-4,
                zlib, zlib-acknowledgement, zpl-1-1, zpl-2-0,
                zpl-2-1.
            readme (str):
                README template name.
                Valid template name(s) are: default.
        """

        default_branch: str = proto.Field(
            proto.STRING,
            number=1,
        )
        gitignores: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        license_: str = proto.Field(
            proto.STRING,
            number=3,
        )
        readme: str = proto.Field(
            proto.STRING,
            number=4,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    instance: str = proto.Field(
        proto.STRING,
        number=3,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )
    uris: URIs = proto.Field(
        proto.MESSAGE,
        number=9,
        message=URIs,
    )
    initial_config: InitialConfig = proto.Field(
        proto.MESSAGE,
        number=10,
        message=InitialConfig,
    )


class ListInstancesRequest(proto.Message):
    r"""ListInstancesRequest is the request to list instances.

    Attributes:
        parent (str):
            Required. Parent value for
            ListInstancesRequest.
        page_size (int):
            Requested page size. Server may return fewer
            items than requested. If unspecified, server
            will pick an appropriate default.
        page_token (str):
            A token identifying a page of results the
            server should return.
        filter (str):
            Filter for filtering results.
        order_by (str):
            Hint for how to order the results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListInstancesResponse(proto.Message):
    r"""

    Attributes:
        instances (MutableSequence[google.cloud.securesourcemanager_v1.types.Instance]):
            The list of instances.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    instances: MutableSequence["Instance"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Instance",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetInstanceRequest(proto.Message):
    r"""GetInstanceRequest is the request for getting an instance.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateInstanceRequest(proto.Message):
    r"""CreateInstanceRequest is the request for creating an
    instance.

    Attributes:
        parent (str):
            Required. Value for parent.
        instance_id (str):
            Required. ID of the instance to be created.
        instance (google.cloud.securesourcemanager_v1.types.Instance):
            Required. The resource being created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    instance_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    instance: "Instance" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Instance",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteInstanceRequest(proto.Message):
    r"""DeleteInstanceRequest is the request for deleting an
    instance.

    Attributes:
        name (str):
            Required. Name of the resource.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class ListRepositoriesRequest(proto.Message):
    r"""ListRepositoriesRequest is request to list repositories.

    Attributes:
        parent (str):
            Required. Parent value for
            ListRepositoriesRequest.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            A token identifying a page of results the
            server should return.
        filter (str):
            Optional. Filter results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListRepositoriesResponse(proto.Message):
    r"""

    Attributes:
        repositories (MutableSequence[google.cloud.securesourcemanager_v1.types.Repository]):
            The list of repositories.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    repositories: MutableSequence["Repository"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Repository",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetRepositoryRequest(proto.Message):
    r"""GetRepositoryRequest is the request for getting a repository.

    Attributes:
        name (str):
            Required. Name of the repository to retrieve. The format is
            ``projects/{project_number}/locations/{location_id}/repositories/{repository_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateRepositoryRequest(proto.Message):
    r"""CreateRepositoryRequest is the request for creating a
    repository.

    Attributes:
        parent (str):
            Required. The project in which to create the repository.
            Values are of the form
            ``projects/{project_number}/locations/{location_id}``
        repository (google.cloud.securesourcemanager_v1.types.Repository):
            Required. The resource being created.
        repository_id (str):
            Required. The ID to use for the repository, which will
            become the final component of the repository's resource
            name. This value should be 4-63 characters, and valid
            characters are /[a-z][0-9]-/.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    repository: "Repository" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Repository",
    )
    repository_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteRepositoryRequest(proto.Message):
    r"""DeleteRepositoryRequest is the request to delete a
    repository.

    Attributes:
        name (str):
            Required. Name of the repository to delete. The format is
            projects/{project_number}/locations/{location_id}/repositories/{repository_id}.
        allow_missing (bool):
            Optional. If set to true, and the repository
            is not found, the request will succeed but no
            action will be taken on the server.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
