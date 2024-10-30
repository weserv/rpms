FROM fedora:41 AS build
LABEL maintainer="Kleis Auke Wolthuizen <info@kleisauke.nl>"

RUN dnf update -y \
    && dnf install -y mock findutils \
    && dnf clean all

VOLUME ["/rpmbuild", "/rpms"]

COPY .mock /etc/mock

# Configure mock
RUN useradd -u 1000 -G mock builder \
    && chmod g+w /etc/mock/*.cfg \
    && install -g mock -m 2775 -d /rpmbuild/cache/mock
