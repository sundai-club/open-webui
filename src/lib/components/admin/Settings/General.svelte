<script lang="ts">
	import {
		getCommunitySharingEnabledStatus,
		getWebhookUrl,
		toggleCommunitySharingEnabledStatus,
		updateWebhookUrl
	} from '$lib/apis';
	import {
		getAdminConfig,
		getDefaultUserRole,
		getJWTExpiresDuration,
		getSignUpEnabledStatus,
		toggleSignUpEnabledStatus,
		updateAdminConfig,
		updateDefaultUserRole,
		updateJWTExpiresDuration
	} from '$lib/apis/auths';
	import Switch from '$lib/components/common/Switch.svelte';
	import { onMount, getContext } from 'svelte';

	const i18n = getContext('i18n');

	export let saveHandler: Function;

	let adminConfig = null;
	let webhookUrl = '';

	const updateHandler = async () => {
		webhookUrl = await updateWebhookUrl(localStorage.token, webhookUrl);
		const res = await updateAdminConfig(localStorage.token, adminConfig);

		if (res) {
			toast.success(i18n.t('Settings updated successfully'));
		} else {
			toast.error(i18n.t('Failed to update settings'));
		}
	};

	onMount(async () => {
	await Promise.all([
		(async () => {
			adminConfig = await getAdminConfig(localStorage.token);
		})(),

		(async () => {
			webhookUrl = await getWebhookUrl(localStorage.token);
		})()
	]);
});
	
</script>

<form
	class="flex flex-col h-full justify-between space-y-3 text-sm"
	on:submit|preventDefault={() => {
		updateHandler();
		saveHandler();
	}}
>
	<div class=" space-y-3 overflow-y-scroll scrollbar-hidden h-full">
		{#if adminConfig !== null}
			<div>
				<div class=" my-3 text-sm font-medium">{$i18n.t('General Settings')}</div>
				<div class="  flex w-full justify-between pr-2">
					<div class=" self-center text-xs font-medium">{$i18n.t('Enable New Sign Ups')}</div>

					<Switch bind:state={adminConfig.ENABLE_SIGNUP} />
				</div>

				<div class="  my-3 flex w-full justify-between">
					<div class=" self-center text-xs font-medium">{$i18n.t('Default User Role')}</div>
					<div class="flex items-center relative">
						<select
							class="dark:bg-gray-900 w-fit pr-8 rounded px-2 text-xs bg-transparent outline-none text-right"
							bind:value={adminConfig.DEFAULT_USER_ROLE}
							placeholder="Select a role"
						>
							<option value="pending">{$i18n.t('pending')}</option>
							<option value="user">{$i18n.t('user')}</option>
							<option value="admin">{$i18n.t('admin')}</option>
						</select>
					</div>
				</div>

				<hr class=" dark:border-gray-850 my-2" />

				<div class="my-3 flex w-full items-center justify-between pr-2">
					<div class=" self-center text-xs font-medium">
						{$i18n.t('Show Admin Details in Account Pending Overlay')}
					</div>

					<Switch bind:state={adminConfig.SHOW_ADMIN_DETAILS} />
				</div>

				<div class="my-3 flex w-full items-center justify-between pr-2">
					<div class=" self-center text-xs font-medium">{$i18n.t('Enable Community Sharing')}</div>

					<Switch bind:state={adminConfig.ENABLE_COMMUNITY_SHARING} />
				</div>

				<hr class=" dark:border-gray-850 my-2" />

				<div class=" w-full justify-between">
					<div class="flex w-full justify-between">
						<div class=" self-center text-xs font-medium">{$i18n.t('JWT Expiration')}</div>
					</div>

					<div class="flex mt-2 space-x-2">
						<input
							class="w-full rounded-lg py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none"
							type="text"
							placeholder={`e.g.) "30m","1h", "10d". `}
							bind:value={adminConfig.JWT_EXPIRES_IN}
						/>
					</div>

					<div class="mt-2 text-xs text-gray-400 dark:text-gray-500">
						{$i18n.t('Valid time units:')}
						<span class=" text-gray-300 font-medium"
							>{$i18n.t("'s', 'm', 'h', 'd', 'w' or '-1' for no expiration.")}</span
						>
					</div>
				</div>

				<hr class=" dark:border-gray-850 my-2" />

				<div class=" w-full justify-between">
					<div class="flex w-full justify-between">
						<div class=" self-center text-xs font-medium">{$i18n.t('Webhook URL')}</div>
					</div>

					<div class="flex mt-2 space-x-2">
						<input
							class="w-full rounded-lg py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none"
							type="text"
							placeholder={`https://example.com/webhook`}
							bind:value={webhookUrl}
						/>
					</div>
				</div>


				<div class=" my-3 text-sm font-medium">{$i18n.t('Mask Settings')}</div>
				<!-- <div class="  flex w-full justify-between pr-2">
					<div class=" self-center text-xs font-medium">{$i18n.t('Mask Name?')}</div>
		
					<Switch bind:state={adminConfig.MASK_NAME} />
				</div> -->
				<div class="  flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_COMPANY} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Company')}</div>
				</div>
				<div class="  flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_LOCATION} />
					<div class="mx-2  self-center text-xs font-medium">{$i18n.t('Mask Location')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_CREDIT_CARD} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Credit Card')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_CRYPTO} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Crypto')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_EMAIL_ADDRESS} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Email Address')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_IBAN_CODE} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask IBAN Code')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_IP_ADDRESS} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask IP Address')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_PERSON} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Person')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_PHONE_NUMBER} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Phone Number')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_US_SSN} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask US SSN')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_US_BANK_NUMBER} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask US Bank Number')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_CREDIT_CARD_RE} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Credit Card RE')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_UUID} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask UUID')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_EMAIL_ADDRESS_RE} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask Email Address RE')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_US_SSN_RE} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask US SSN RE')}</div>
				</div>
				<div class="flex w-full justify-start pr-2">
					<Switch bind:state={adminConfig.MASK_URL} />
					<div class="mx-2 self-center text-xs font-medium">{$i18n.t('Mask URL')}</div>
				</div>
			</div>
		{/if}
	</div>

	<div class="flex justify-end pt-3 text-sm font-medium">
		<button
			class=" px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg"
			type="submit"
		>
			{$i18n.t('Save')}
		</button>
	</div>
</form>
