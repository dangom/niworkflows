#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
import os

from .utils import _copyxform

from niworkflows.nipype.interfaces.ants.resampling import ApplyTransforms
from niworkflows.nipype.interfaces.ants.registration import Registration


class FixHeaderApplyTransforms(ApplyTransforms):
    """
    A replacement for nipype.interfaces.ants.resampling.ApplyTransforms that
    fixes the resampled image header to match the xform of the reference
    image
    """

    def _run_interface(self, runtime, correct_return_codes=(0,)):
        # Run normally
        runtime = super(FixHeaderApplyTransforms, self)._run_interface(
            runtime, correct_return_codes)

        _copyxform(self.inputs.reference_image,
                   os.path.abspath(self._gen_filename('output_image')),
                   message=self.__class__.__name__)
        return runtime


class FixHeaderRegistration(Registration):
    """
    A replacement for nipype.interfaces.ants.registration.Registration that
    fixes the resampled image header to match the xform of the reference
    image
    """

    def _run_interface(self, runtime, correct_return_codes=(0,)):
        # Run normally
        runtime = super(FixHeaderRegistration, self)._run_interface(
            runtime, correct_return_codes)

        _copyxform(self.inputs.fixed_image[0],
                   os.path.abspath(self._get_outputfilenames(inverse=False)),
                   message=self.__class__.__name__)
        return runtime
