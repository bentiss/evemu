/*
 * Copyright (C) 2010-2012 Canonical Ltd.
 * Copyright (C) 2010 Henrik Rydberg <rydberg@euromail.se>
 *
 * This library is free software: you can redistribute it and/or modify it 
 * under the terms of the GNU Lesser General Public License version 3
 * as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but 
 * WITHOUT ANY WARRANTY; without even the implied warranties of 
 * MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
 * PURPOSE.  See the GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef EVEMU_IMPL_H
#define EVEMU_IMPL_H

#include <evemu.h>
#include <libevdev/libevdev.h>

#define EVPLAY_NBITS	KEY_CNT
#define EVPLAY_NBYTES	((EVPLAY_NBITS + 7) / 8)

struct evemu_device {
	unsigned int version;
	unsigned int fd_changed;
	struct libevdev *evdev;
	struct libevdev_uinput *udev;
	int pbytes, mbytes[EV_CNT];
};

#endif
